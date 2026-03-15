# app/task_queue/instance.py
from celery import Celery
from .config import celery_config
from .queue import cpu_bound_queue, io_bound_queue


celery_app = Celery(
    celery_config.app_name,
    broker=celery_config.broker_url,
    backend=celery_config.result_backend_url,
)
"""
Celery application instance configured via application settings.

This instance provides the foundational task queue interface for all
background task execution and result storage operations.
"""

# Updates the application's operational settings whose serialization, scheduling,
# and result expiration semantics are dictated by the `CeleryConfig` settings.
celery_app.conf.update(
    task_serializer=celery_config.task_serializer,
    result_serializer=celery_config.result_serializer,
    accept_content=celery_config.accept_content,
    timezone=celery_config.timezone,
    enable_utc=celery_config.enable_utc,
    result_expires=celery_config.result_expires,
    task_queues=(cpu_bound_queue, io_bound_queue),
)


# Automatically discover and register Celery tasks from the specified modules.
# This tells Celery to scan the 'app.task_queue.tasks' module and any submodules
# for functions decorated with @celery_app.task, making them available
# for background execution by the worker processes.
# Using autodiscover_tasks is the recommended way to register tasks
# without having to manually import each task module.
celery_app.autodiscover_tasks(["app.task_queue.tasks"])