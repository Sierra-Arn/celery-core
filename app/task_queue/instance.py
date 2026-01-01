# app/task_queue/instance.py
from celery import Celery
from .config import celery_config


# Initialize the Celery application instance.
# This is a singleton object that holds the configuration and connection
# to the Redis broker and result backend. It should be imported and used
# throughout the application to define tasks and manage the worker lifecycle.
celery_app = Celery(
    celery_config.app_name,
    broker=celery_config.broker_url,
    backend=celery_config.result_backend_url,
)

# Update Celery configuration with additional settings.
celery_app.conf.update(
    task_serializer=celery_config.task_serializer,
    result_serializer=celery_config.result_serializer,
    accept_content=celery_config.accept_content,
    timezone=celery_config.timezone,
    enable_utc=celery_config.enable_utc,
    result_expires=celery_config.result_expires,
)

# Configure task queues for different workloads.
# This defines two named queues: one for CPU-bound tasks and another for I/O-bound tasks.
#
# Note: `celery_app.conf.task_queues` is a dynamically generated attribute in Celery.
# It is not a static field defined at the class level, which is why static analyzers (like Pylance in VS Code)
# may underline it as unresolved. However, this is perfectly valid and documented behavior.
# The configuration is applied at runtime and will work as expected.
celery_app.conf.task_queues = {
    celery_config.cpu_bound_queue_name: {
        "exchange": celery_config.cpu_bound_queue_name,
        "routing_key": celery_config.cpu_bound_queue_name,
        "queue_arguments": {
            "x-max-priority": celery_config.cpu_bound_queue_max_priority,
        },
    },
    celery_config.io_bound_queue_name: {
        "exchange": celery_config.io_bound_queue_name,
        "routing_key": celery_config.io_bound_queue_name,
        "queue_arguments": {
            "x-max-priority": celery_config.io_bound_queue_max_priority,
        },
    },
}

# Automatically discover and register Celery tasks from the specified modules.
# This tells Celery to scan the 'app.services' module and any submodules
# for functions decorated with @celery_app.task, making them available
# for asynchronous execution by the worker processes.
# Using autodiscover_tasks is the recommended way to register tasks
# without having to manually import each task module.
celery_app.autodiscover_tasks(['app.services'])