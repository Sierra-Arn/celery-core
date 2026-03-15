# app/task_queue/workers/instance.py
from .schema import WorkerSchema
from ..instance import celery_app


class CeleryWorker:
    """
    A class representing a Celery worker instance.

    Notes
    -----
    Workers can be stateless (executes task without storing execution history) or stateful.
    Stateless approach is used here for simplicity since this is an educational project.
    """

    def __init__(self, config: WorkerSchema):
        """
        Initialize the worker with the given configuration.

        Parameters
        ----------
        config : WorkerConfig
            An instance of WorkerConfig containing all necessary settings for this worker.

        Note:
        -----
        Automatically append @%n to ensure unique worker names when multiple instances
        are running on the same host. Celery will replace %n with a unique number
        for each worker process, preventing naming conflicts.
        """

        self.name = f"{config.name}@%n"
        self.queue_name = config.queue_name
        self.pool = config.pool
        self.concurrency = str(config.concurrency)
        self.prefetch_multiplier = str(config.prefetch_multiplier)
        self.loglevel = config.loglevel
        self.celery_app = celery_app

    def start(self):
        """
        Start the Celery worker with the configured settings.
        """

        worker_args = [
            "worker",
            "--hostname", self.name,
            "--queues", self.queue_name,
            "--pool", self.pool,
            "--concurrency", self.concurrency,
            "--prefetch-multiplier", self.prefetch_multiplier,
            "--loglevel", self.loglevel
        ]
        
        self.celery_app.worker_main(argv=worker_args)