# app/task_queue/workers/io_bound.py

# IMPORTANT: gevent monkey patching must be applied BEFORE any other imports.
# `monkey.patch_all()` replaces standard library modules (like socket, threading, time, etc.)
# with gevent-compatible cooperative versions. This allows synchronous-looking code
# to work with gevent's asynchronous, coroutine-based I/O model.
# If imported after standard modules (e.g., after importing Celery, urllib, etc.),
# those modules will continue using blocking I/O.
from gevent import monkey
monkey.patch_all()

from .config import WorkerConfig
from .worker import CeleryWorker
from ..config import celery_config


# Create a configuration instance for the I/O-bound task worker:
# - Listen on the dedicated I/O-bound queue.
# - Uses the 'gevent' pool to leverage cooperative multitasking for I/O operations.
# - Allows higher prefetching to keep the worker busy during I/O waits.
# - Sets concurrency to 100, which is suitable for I/O-bound workloads with high concurrency needs.
io_worker_config = WorkerConfig(
    name = "io_bound_worker",
    queue_name = celery_config.io_bound_queue_name,
    pool = "gevent",
    concurrency = 100,
    prefetch_multiplier = 3,
    loglevel = "INFO"
)

# Initialize the Celery worker instance with the specified configuration.
io_worker = CeleryWorker(io_worker_config)

# Entry point for running the I/O-bound worker directly.
# When this script is executed, it will start a Celery worker configured for I/O-intensive tasks.
if __name__ == "__main__":
    io_worker.start()