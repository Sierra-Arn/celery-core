# app/task_queue/workers/io_bound.py

# IMPORTANT: gevent monkey patching must be applied BEFORE any other imports.
# `monkey.patch_all()` replaces standard library modules (like socket, threading, time, etc.)
# with gevent-compatible cooperative versions. This allows synchronous-looking code
# to work with gevent's asynchronous, coroutine-based I/O model.
# If imported after standard modules (e.g., after importing Celery, urllib, etc.),
# those modules will continue using blocking I/O.
from gevent import monkey
monkey.patch_all()

from .cli import parse_args
from .schema import WorkerSchema
from .instance import CeleryWorker
from ..config import celery_config


# Entry point for running the I/O-bound worker directly.
# When this script is executed, it starts a Celery worker
# configured for I/O-intensive tasks.
if __name__ == "__main__":

    args = parse_args()

    io_worker_config = WorkerSchema(
        name=args.name,
        queue_name=celery_config.io_bound_queue_name,
        pool="gevent",
        concurrency=args.concurrency,
        prefetch_multiplier=args.prefetch_multiplier,
        loglevel=args.loglevel,
    )
    """
    Configuration for the I/O-bound task worker.

    Listens on the dedicated I/O-bound queue and uses the gevent pool
    for efficient cooperative multitasking during I/O waits,
    allowing high concurrency without spawning additional processes.
    """

    io_worker = CeleryWorker(io_worker_config)
    """
    Celery worker instance configured for I/O-intensive task execution.
    """

    io_worker.start()