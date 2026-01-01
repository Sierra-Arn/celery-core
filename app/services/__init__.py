# app/services/__init__.py
import time
import random
from typing import Any
import gevent
from ..task_queue.instance import celery_app, celery_config


class MockTaskService:
    """
    Mock service demonstrating Celery task execution patterns.

    Simulates typical operations with different computational characteristics:
    - CPU-intensive operations (use dedicated CPU-bound queue)
    - I/O-intensive operations (use dedicated I/O-bound queue with gevent)
    """

    @celery_app.task(
        bind=True, # Bind the task instance to allow calling class methods as Celery tasks
        name="mock_task_service.run_cpu_intensive_task",
        queue=celery_config.cpu_bound_queue_name,
        autoretry_for=(Exception,),     # Retry on any exception
        retry_kwargs={
            'max_retries': 3,           # Maximum 3 retries
            'countdown': 20             # Time in seconds between retry attempts
        }     
    )
    def run_cpu_intensive_task(self, duration: float) -> dict[str, Any]:
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
        
        # Randomly raise an exception to trigger retry behavior
        if random.random() < 0.3:  # 30% chance of failure
            raise RuntimeError("Simulated CPU-intensive task failure")
        
        return {
            "task_type": "cpu_intensive",
            "duration": duration,
            "processing_time": time.time()
        }

    @celery_app.task(
        bind=True, # Bind the task instance to allow calling class methods as Celery tasks
        name="mock_task_service.run_io_intensive_task",
        queue=celery_config.io_bound_queue_name,
        autoretry_for=(Exception,),         # Retry on any exception
        retry_kwargs={
            'max_retries': 5,           # Maximum 5 retries
            'countdown': 5              # Time in seconds between retry attempts
        }  
    )
    def run_io_intensive_task(self, duration: float) -> dict[str, Any]:
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

        # Simulate I/O-intensive work with non-blocking delays using gevent
        gevent.sleep(duration)
        
        # Randomly raise an exception to trigger retry behavior
        if random.random() < 0.2:  # 20% chance of failure
            raise ConnectionError("Simulated network timeout")
        
        return {
            "task_type": "io_intensive",
            "duration": duration,
            "completion_time": time.time()
        }