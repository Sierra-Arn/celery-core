# app/task_queue/queue.py
from kombu import Queue
from .config import celery_config
from .exchange import tasks_exchange


cpu_bound_queue = Queue(
    celery_config.cpu_bound_queue_name,
    exchange=tasks_exchange,
    routing_key=celery_config.cpu_bound_queue_name,
)
"""
Queue for CPU-intensive tasks configured via application settings.

Bound to the shared exchange via a direct routing key matching the queue name.
Following the standard direct exchange pattern, the routing key is intentionally
equal to the queue name — the exchange delivers a message to this queue only
when the producer's routing key exactly matches ``celery_config.cpu_bound_queue_name``.

Since Redis is used as the broker, true message priority is not supported.
The workaround via ``task_queue_max_priority`` does not implement real priority —
it simply creates N separate sub-queues under the hood, which does not guarantee
ordering by importance. Therefore, tasks in this queue are consumed in FIFO order.
"""

io_bound_queue = Queue(
    celery_config.io_bound_queue_name,
    exchange=tasks_exchange,
    routing_key=celery_config.io_bound_queue_name,
)
"""
Queue for I/O-intensive tasks configured via application settings.

Bound to the shared exchange via a direct routing key matching the queue name.
Following the standard direct exchange pattern, the routing key is intentionally
equal to the queue name — the exchange delivers a message to this queue only
when the producer's routing key exactly matches ``celery_config.io_bound_queue_name``.

Since Redis is used as the broker, true message priority is not supported.
The workaround via ``task_queue_max_priority`` does not implement real priority —
it simply creates N separate sub-queues under the hood, which does not guarantee
ordering by importance. Therefore, tasks in this queue are consumed in FIFO order.
"""