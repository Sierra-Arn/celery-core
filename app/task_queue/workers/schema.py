# app/task_queue/workers/schema.py
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


class WorkerSchema(BaseModel):
    """
    Configuration schema for a Celery worker instance.

    Attributes
    ----------
    queue_name : str
        The name of the specific task queue this worker should listen to.
    name : str
        The name of this worker instance. Used for identification in logs and monitoring.
    pool : str
        The pool implementation to use for executing tasks. Common values:
        - ``"prefork"`` : Uses multiprocessing.
        - ``"gevent"``  : Uses cooperative multitasking.
        - ``"solo"``    : Uses single-threaded, single-process execution.
    concurrency : int
        The number of concurrent worker processes or threads.
    prefetch_multiplier : int
        The number of tasks a worker will prefetch from the queue at once.
    loglevel : Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        Logging level for the worker.
    """

    name: str
    queue_name: str
    pool: str
    concurrency: int = Field(default=1, ge=1)
    prefetch_multiplier: int = Field(default=1, ge=1)
    loglevel: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    model_config = ConfigDict(
            frozen=True,
            extra="forbid",
            json_schema_extra={
                "examples": [
                    {
                        "name": "cpu_worker",
                        "queue_name": "cpu-bound",
                        "pool": "prefork",
                        "concurrency": 4,
                        "prefetch_multiplier": 1,
                        "loglevel": "INFO",
                    },
                    {
                        "name": "io_worker",
                        "queue_name": "io-bound",
                        "pool": "gevent",
                        "concurrency": 10,
                        "prefetch_multiplier": 1,
                        "loglevel": "INFO",
                    },
                ]
            },
        )