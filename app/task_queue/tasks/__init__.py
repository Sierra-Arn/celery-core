# app/task_queue/tasks/__init__.py
import time
import random
from typing import Any
import gevent
from ..instance import celery_app
from ..config import celery_config


@celery_app.task(
    name="run_io_intensive_task",
    queue=celery_config.io_bound_queue_name,
    # Retry on any exception — I/O failures are often temporary
    # (e.g., network timeout, overloaded database) and may resolve on their own.
    autoretry_for=(Exception,),
    retry_kwargs={
        "max_retries": 5,
        # Wait before retrying to give the external service time to recover.
        "countdown": 5,
    },
)
def run_io_intensive_task(duration: float) -> dict[str, Any]:
    """
    Simulate running I/O-intensive operation (e.g., API calls, database queries).

    Task is routed to the I/O-bound queue and processed by workers using gevent
    for efficient cooperative multitasking during I/O waits.

    Parameters
    ----------
    duration : float
        Duration of the simulated I/O-intensive work in seconds.

    Returns
    -------
    dict[str, Any]
        Operation result with timing information.
    """
    # Simulate I/O-intensive work with a non-blocking delay using gevent
    gevent.sleep(duration)

    # Randomly raise an exception to trigger retry behavior.
    # Simulates a temporarily overloaded database — after a short wait,
    # some existing connections may be released, freeing up capacity
    # for this request to succeed on the next attempt.
    if random.random() < 0.2:  # 20% chance of failure
        raise ConnectionError("Simulated database overload")

    return {
        "task_type": "io_intensive",
        "duration": duration,
        "completion_time": time.time(),
    }


@celery_app.task(
    name="run_cpu_intensive_task",
    queue=celery_config.cpu_bound_queue_name,
    # No retry logic — CPU-bound failures are typically caused by bugs in code
    # or invalid input data, neither of which will resolve itself on the next attempt.
)
def run_cpu_intensive_task(duration: float) -> dict[str, Any]:
    """
    Simulate running CPU-intensive computation.

    Task is routed to the CPU-bound queue and processed by dedicated workers
    using multiprocessing to avoid Python's GIL limitations.

    Parameters
    ----------
    duration : float
        Duration of the simulated CPU-intensive work in seconds.

    Returns
    -------
    dict[str, Any]
        Computation result with performance metrics.
    """

    # Simulate CPU-intensive work with a sleep for the specified duration
    time.sleep(duration)

    # Randomly raise an exception to simulate a task failure
    # and verify Celery's error handling behavior in the absence of retry logic.
    if random.random() < 0.3:  # 30% chance of failure
        raise RuntimeError("Simulated CPU-intensive task failure")

    return {
        "task_type": "cpu_intensive",
        "duration": duration,
        "processing_time": time.time(),
    }


