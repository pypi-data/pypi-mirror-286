import json
import logging
import time
from hashlib import sha256
from queue import Empty, Queue
from random import randint
from textwrap import dedent

from dramatiq.broker import Broker, Consumer, MessageProxy
from dramatiq.common import compute_backoff, current_millis, dq_name
from dramatiq.errors import ConnectionError
from dramatiq.message import Message
from dramatiq.results import Results
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, Notify, quote_ident
from psycopg2.extras import Json

from .results import PostgresBackend
from .utils import (
    QueryManager,
    check_conn,
    getconn,
    make_pool,
    raise_connection_error,
    retry_pg,
    tidy4json,
    transaction,
    wait_for_notifies,
)

logger = logging.getLogger(__name__)


def purge(curs, max_age="30 days"):
    # Delete old messages. Returns deleted messages.

    curs.execute(QUERIES.PURGE, (max_age,))
    return curs.rowcount


class PostgresBroker(Broker):
    def __init__(
        self,
        *,
        pool=None,
        url="",
        results=True,
        schema=None,
        prefix=None,
        **kw
    ):
        super(PostgresBroker, self).__init__(**kw)
        if pool and url:
            raise ValueError("You can't set both pool and URL!")

        if not pool:
            self.pool = make_pool(url)
        else:
            # Receive a pool object to have an I/O less __init__.
            self.pool = pool
        self.backend = None
        if results:
            self.backend = PostgresBackend(
                pool=self.pool, schema=schema, prefix=prefix
            )
            self.add_middleware(Results(backend=self.backend))

        QUERIES.build_queries(schema, prefix)

    def consume(self, queue_name, prefetch=1, timeout=30000):
        return PostgresConsumer(
            pool=self.pool,
            queue_name=queue_name,
            prefetch=prefetch,
            timeout=timeout,
        )

    def declare_queue(self, queue_name):
        if queue_name not in self.queues:
            self.emit_before("declare_queue", queue_name)
            self.queues[queue_name] = True
            # Actually do nothing in Postgres since all queues are stored in
            # the same table.
            self.emit_after("declare_queue", queue_name)

            delayed_name = dq_name(queue_name)
            self.delay_queues.add(delayed_name)
            self.emit_after("declare_delay_queue", delayed_name)

    @retry_pg
    def enqueue(self, message, *, delay=None):
        if delay:
            message = message.copy(queue_name=dq_name(message.queue_name))
            message.options["eta"] = current_millis() + delay

        q = message.queue_name
        insert = (
            QUERIES.ENQUEUE,
            (
                q,
                message.message_id,
                Json(tidy4json(message)),
                message.message_id,
            ),
        )

        logger.debug("Upserting %s in queue %s.", message.message_id, q)
        self.emit_before("enqueue", message, delay)
        with transaction(self.pool) as curs:
            curs.execute(*insert)
        self.emit_after("enqueue", message, delay)
        return message


class PostgresConsumer(Consumer):
    def __init__(self, *, pool, queue_name, prefetch, timeout, **kw):
        self._consume_conn = None
        self._listen_conn = None
        self.notifies = []
        self.pool = pool
        self.queue_name = queue_name
        self.timeout = timeout // 1000
        self.unlock_q = Queue()
        self.in_processing = set()
        self.prefetch = prefetch
        self.misses = 0

    @raise_connection_error
    def __next__(self):
        # This function is executed each second.

        # First, open connexion and fetch missed notifies from table.
        if self._listen_conn is None:
            # Before reading from LISTEN, scan queue for missed messages.
            self.notifies = self.fetch_pending_notifies()
            logger.debug(
                "Found %s pending messages in queue %s.",
                len(self.notifies),
                self.queue_name,
            )

        processing = len(self.in_processing)
        if processing >= self.prefetch:
            # Wait and don't consume the message, other worker will be faster
            self.misses, backoff_ms = compute_backoff(
                self.misses, max_backoff=1000
            )
            logger.debug(
                f"Too many messages in processing:"
                f" {processing}"
                f" sleeping {backoff_ms}"
            )
            time.sleep(backoff_ms / 1000)
            return None

        if not self.notifies:
            # Then, fetch notifies from Pg connexion.
            self.poll_for_notify()

        if not self.notifies and not randint(0, 300):
            # If notifies are consumed, randomly poll for crashed messages.
            # Since we're called each second, this condition limits polling to
            # one SELECT every five minutes of inactivity.
            self.notifies[:] = self.fetch_pending_notifies()

        # If we have some notifies, loop to find one todo.
        while self.notifies:
            notify = self.notifies.pop(0)
            if "kwargs" in notify.payload:
                full_payload = notify.payload
            else:
                truncated_payload = json.loads(notify.payload)
                full_payload = self.fetch_by_id(
                    truncated_payload["message_id"]
                )
            message = Message.decode(full_payload.encode("utf-8"))
            if self.consume_one(message):
                self.in_processing.add(message.message_id)
                return MessageProxy(message)
            else:
                logger.debug(
                    "Message %s already consumed. Skipping.",
                    message.message_id,
                )

        # No message to process. Let's clean locks.
        self.purge_locks()

        # We have nothing to do, let's see if the queue needs some cleaning.
        self.auto_purge()

    @raise_connection_error
    def ack(self, message):
        # This function is executed in worker thread!

        with transaction(self.pool) as curs:
            channel = f"dramatiq.{message.queue_name}.ack"
            payload = tidy4json(message)
            self.unlock_q.put_nowait(message)
            logger.debug(
                "Notifying %s for ACK %s.", channel, message.message_id
            )
            # dramatiq always ack a message, even if it has been requeued by
            # the Retries middleware. Thus, only update message in state
            # `consumed`.
            curs.execute(
                QUERIES.ACK,
                (
                    Json(payload),
                    message.message_id,
                    message.queue_name,
                    channel,
                    message.message_id,
                ),
            )
        self.in_processing.remove(message.message_id)

    @raise_connection_error
    def auto_purge(self):
        # Automatically purge messages every 100k iteration. Dramatiq defaults
        # to 1s. This mean about 1 purge for 28h idle.
        if randint(0, 100_000):
            return
        logger.debug("Randomly triggering garbage collector.")
        with transaction(self._consume_conn) as curs:
            deleted = purge(curs)
        logger.info("Purged %d messages in all queues.", deleted)

    def close(self):
        if self._listen_conn:
            self.pool.putconn(self._listen_conn)
            self._listen_conn = None

        if self._consume_conn:
            self.pool.putconn(self._consume_conn)
            self._consume_conn = None

    def get_consume_conn(self):
        # Ensure connection used for message consumption is steady.
        if self._consume_conn is not None:
            try:
                check_conn(self._consume_conn)
            except ConnectionError:
                logger.info("Connection closed. Reconnecting...")
                self.pool.putconn(self._consume_conn)
                self._consume_conn = None

        if self._consume_conn is None:
            logger.debug("Asking new connection for message consumption.")
            self._consume_conn = getconn(self.pool)

        return self._consume_conn

    @raise_connection_error
    def get_listen_conn(self):
        # Opens listening connection with proper configuration.
        if self._listen_conn is not None:
            try:
                return check_conn(self._listen_conn)
            except ConnectionError:
                logger.info("Connection closed. Reconnecting...")
                self.pool.putconn(self._listen_conn)
                self._listen_conn = None

        self._listen_conn = conn = getconn(self.pool)
        # This is for NOTIFY consistency, according to psycopg2 doc.
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        channel = quote_ident(f"dramatiq.{self.queue_name}.enqueue", conn)
        with conn.cursor() as curs:
            logger.debug("Listening on channel %s.", channel)
            curs.execute(f"LISTEN {channel};")
        return self._listen_conn

    @raise_connection_error
    def consume_one(self, message):
        if message.message_id in self.in_processing:
            logger.debug("%s already consumed by self.", message.message_id)
            return

        # Race to process message.
        with transaction(self.get_consume_conn()) as curs:
            lock = message_lock(message)
            curs.execute(QUERIES.CONSUME_ONE, (message.message_id, lock))
            # If no row was updated, this mean another worker has consumed it.
            if curs.rowcount:
                logger.info(
                    "Consumed %s@%s.", message.message_id, message.queue_name
                )
            return 1 == curs.rowcount

    @raise_connection_error
    def nack(self, message):
        # This function is executed in worker thread.

        with transaction(self.pool) as curs:
            # Use the same channel as ack. Actually means done.
            channel = f"dramatiq.{message.queue_name}.ack"
            self.unlock_q.put_nowait(message)
            logger.debug(
                "Notifying %s for NACK %s.", channel, message.message_id
            )
            payload = tidy4json(message)
            curs.execute(
                QUERIES.NACK,
                (
                    Json(payload),
                    message.message_id,
                    message.queue_name,
                    channel,
                    message.message_id,
                ),
            )
        self.in_processing.remove(message.message_id)

    @raise_connection_error
    def fetch_by_id(self, message_id):
        logger.debug(
            "Retrieving truncated message %s in %s.",
            message_id,
            self.queue_name,
        )
        # Get or open connection.
        conn = self.get_consume_conn()
        with transaction(conn) as curs:
            curs.execute(QUERIES.FETCH_BY_ID, (message_id,))
            return curs.fetchone()[0]

    @raise_connection_error
    def fetch_pending_notifies(self):
        logger.debug("Polling for lost messages in %s.", self.queue_name)
        # Get or open connection.
        conn = self.get_listen_conn()
        # We may have received a notify between LISTEN and SELECT of pending
        # messages. That's not a problem because we are able to skip spurious
        # notifies.
        channel = f"dramatiq.{self.queue_name}.enqueue"
        with transaction(conn) as curs:
            curs.execute(QUERIES.FETCH_PENDING, (self.queue_name,))
            return [Notify(pid=0, channel=channel, payload=r[0]) for r in curs]

    @raise_connection_error
    def poll_for_notify(self):
        self.notifies += wait_for_notifies(
            self.get_listen_conn(), self.timeout
        )

    @raise_connection_error
    def purge_locks(self):
        with transaction(self.get_consume_conn()) as curs:
            while True:
                try:
                    message = self.unlock_q.get(block=False)
                except Empty:
                    return
                lock = message_lock(message)
                logger.debug(
                    "Unlocking %s@%s (%s).",
                    message.message_id,
                    message.queue_name,
                    lock,
                )
                curs.execute(
                    dedent(
                        """\
                SELECT pg_advisory_unlock(%s);
                """
                    ),
                    (lock,),
                )
                self.unlock_q.task_done()

    @raise_connection_error
    def requeue(self, messages):
        messages = list(messages)
        if not len(messages):
            return

        logger.debug("Batch update of messages for requeue.")
        with transaction(self.get_consume_conn()) as curs:
            curs.execute(
                QUERIES.REQUEUE, (tuple(m.message_id for m in messages),)
            )
            # We don't bother about locks, because requeue occurs on worker
            # stop.


_max_positive_int = 2**63


def message_lock(message):
    # create sha256 hash from input and create a 64 bit int from it, using
    # 16 hex char. any 16 char range is ok. it takes the center ones
    global_id = message.queue_name + str(message.message_id)
    hex = sha256(global_id.encode("utf-8")).hexdigest()
    unsigned = int(hex[24:40], 16)
    # PostgreSQL lock is a signed int on 64 bytes. Shift unsigned value from
    # interval [0..2**64] to interval [-2**63..2**63].
    return unsigned - _max_positive_int


QUERIES = QueryManager(
    dict(
        ACK=dedent(
            """\
        WITH updated AS (
            UPDATE {schema}.{tablename}
                SET "state" = 'done', message = %s
            WHERE message_id = %s
                AND queue_name = %s
                AND state = 'consumed'
            RETURNING message
        )
        SELECT
            pg_notify(%s,
                CASE WHEN octet_length(message::text) >= 8000
                THEN jsonb_build_object('message_id', %s)::text
                ELSE message::text
                END
            )
        FROM updated;
        """
        ),
        CONSUME_ONE=dedent(
            """\
        UPDATE {schema}.{tablename}
            SET "state" = 'consumed',
                mtime = (NOW() AT TIME ZONE 'UTC')
            WHERE message_id = %s
            AND state IN ('queued', 'consumed')
            AND pg_try_advisory_lock(%s);
        """
        ),
        ENQUEUE=dedent(
            """\
        WITH enqueued AS (
            INSERT INTO {schema}.{tablename}
            (queue_name, message_id, "state", message)
            VALUES (%s, %s, 'queued', %s)
            ON CONFLICT (message_id)
                DO UPDATE SET
                    "state" = 'queued',
                    message = EXCLUDED.message,
                    queue_name = EXCLUDED.queue_name
            RETURNING queue_name, message
        )
        SELECT
            pg_notify('dramatiq.' || queue_name || '.enqueue',
                CASE WHEN octet_length(message::text) >= 8000
                THEN jsonb_build_object('message_id', %s)::text
                ELSE message::text
                END
            )
        FROM enqueued;
        """
        ),  # noqa
        FETCH_PENDING=dedent(
            """\
        SELECT message::text
            FROM {schema}.{tablename}
            WHERE state IN ('queued', 'consumed')
            AND queue_name = %s;
        """
        ),
        FETCH_BY_ID=dedent(
            """\
        SELECT message::text
            FROM {schema}.{tablename}
            WHERE message_id = %s;
        """
        ),
        NACK=dedent(
            """\
        WITH updated AS (
            UPDATE {schema}.{tablename}
                SET "state" = 'rejected', message = %s
            WHERE message_id = %s
                AND queue_name = %s
                AND state <> 'rejected'
            RETURNING message
        )
        SELECT
            pg_notify(%s,
                CASE WHEN octet_length(message::text) >= 8000
                THEN jsonb_build_object('message_id', %s)::text
                ELSE message::text
                END
            )
        FROM updated;
        """
        ),
        PURGE=dedent(
            """\
        DELETE FROM {schema}.{tablename}
        WHERE "state" IN ('done', 'rejected')
        AND mtime <= (NOW() - interval %s);
        """
        ),
        REQUEUE=dedent(
            """\
        UPDATE {schema}.{tablename}
            SET state = 'queued'
        WHERE message_id IN %s;
        """
        ),
    )
)
