# app/task_queue/workers/cpu_bound.py
from .cli import parse_args
from .schema import WorkerSchema
from .instance import CeleryWorker
from ..config import celery_config


args = parse_args()

cpu_worker_config = WorkerSchema(
    name=args.name,
    queue_name=celery_config.cpu_bound_queue_name,
    pool="prefork",
    concurrency=args.concurrency,
    prefetch_multiplier=args.prefetch_multiplier,
    loglevel=args.loglevel,
)
"""
Configuration for the CPU-bound task worker.

Listens on the dedicated CPU-bound queue and uses the prefork pool
to leverage multiprocessing and bypass Python's GIL for parallel execution.
"""


cpu_worker = CeleryWorker(cpu_worker_config)
"""
Celery worker instance configured for CPU-intensive task execution.
"""

# Entry point for running the CPU-bound worker directly.
# When this script is executed, it starts a Celery worker
# configured for CPU-intensive tasks.
if __name__ == "__main__":
    cpu_worker.start()