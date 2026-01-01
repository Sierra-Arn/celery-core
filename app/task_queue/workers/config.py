# app/task_queue/workers/config.py
from typing import ClassVar, Literal
from pydantic import Field
from ..shared import BaseConfig


class WorkerConfig(BaseConfig):
    """
    Configuration for a Celery worker instance.

    Attributes
    ----------
    queue_name : str
        The name of the specific task queue this worker should listen to.
    name : str
        The name of this worker instance. Used for identification in logs and monitoring.
        Default is `"celery_worker"`.
    pool : str
        The pool implementation to use for executing tasks. Common values:
        - `"prefork"`: Uses multiprocessing.
        - `"gevent"`: Uses cooperative multitasking.
        - `"solo"` (default): Uses single-threaded, single-process execution.
    concurrency : int
        The number of concurrent worker processes or threads. Default is `1`.
    prefetch_multiplier : int
        The number of tasks a worker will prefetch from the queue at once. Default is `1`.
    loglevel : Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        Logging level for the worker. Default is `"INFO"`.

    Notes
    -----
    This class inherits from `app.task_queue.shared.base_config.BaseConfig`.
    For details on configuration loading behavior, see its documentation.
    """

    env_prefix: ClassVar[str] = "WORKER_"

    name: str = "celery_worker"
    queue_name: str
    pool: str = "solo"
    concurrency: int = Field(default=1, ge=1)
    prefetch_multiplier: int = Field(default=1, ge=1)
    loglevel: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"