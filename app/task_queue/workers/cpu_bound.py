# app/task_queue/workers/cpu_bound.py
from .config import WorkerConfig
from .worker import CeleryWorker
from ..config import celery_config


# Create a configuration instance for the CPU-bound task worker:
# - Listen on the dedicated CPU-bound queue.
# - Uses the 'prefork' pool to leverage multiple processes and avoid Python's GIL.
# - Limits prefetching to prevent overwhelming the worker with too many tasks at once.
# - Sets concurrency to 1, which is often suitable for CPU-bound workloads.
cpu_worker_config = WorkerConfig(
    name = "cpu_bound_worker",
    queue_name = celery_config.cpu_bound_queue_name,  
    pool = "prefork",
    concurrency = 1,
    prefetch_multiplier = 1,
    loglevel = "INFO"
)

# Initialize the Celery worker instance with the specified configuration.
cpu_worker = CeleryWorker(cpu_worker_config)

# Entry point for running the CPU-bound worker directly.
# When this script is executed, it will start a Celery worker configured for CPU-intensive tasks.
if __name__ == "__main__":
    cpu_worker.start()