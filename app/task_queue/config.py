# app/task_queue/config.py
from typing import ClassVar
from pydantic import Field
from ..shared import BaseConfig
from ..db.config import redis_config


class CeleryConfig(BaseConfig):
    """
    Configuration schema for Celery task queue service.

    Attributes
    ----------
    broker_db_index : int
        Redis database index used for the message broker. Default is 0.
    result_db_index : int
        Redis database index used for storing task results. Default is 1.
    app_name : str
        Name of the Celery application. Used for identification. Default is "celery-core".
    task_serializer : str
        Serializer for task data. Default is "json".
    result_serializer : str
        Serializer for task results. Default is "json".
    accept_content : list[str]
        List of content types accepted by the worker. Default is ["json"].
    timezone : str
        Timezone for scheduling tasks. Default is "UTC".
    enable_utc : bool
        Whether to use UTC for all time-related operations. Default is True.
    result_expires : int
        Number of seconds after which task results expire and are deleted. Default is 60.
    cpu_bound_queue_name : str
        Name of the queue for CPU-intensive tasks. Default is "cpu-bound".
    io_bound_queue_name : str
        Name of the queue for I/O-intensive tasks. Default is "io-bound".
    exchange_name : str
        Name of the shared exchange that routes messages to both task queues. Default is "tasks".
        
    Notes
    -----
    This class inherits from `app.task_queue.shared.base_config.BaseConfig`.
    For details on configuration loading behavior, see its documentation.

    Note: difference between `enable_utc` and `timezone`
    -----
    enable_utc: 
        Controls Celery's internal timekeeping — all operations use UTC for consistency across systems.
    timezone: 
        Controls how timestamps appear in logs and how cron schedules (via Celery Beat) are interpreted.

    For instance, if timezone="Europe/Paris", a task scheduled for "09:00" runs at 09:00 Paris time 
    — even though internal operations remain in UTC.
    """

    env_prefix: ClassVar[str] = "CELERY_"

    broker_db_index: int = Field(default=0, ge=0)
    result_db_index: int = Field(default=1, ge=0)
    app_name: str = "celery-core"
    task_serializer: str = "json"
    result_serializer: str = "json"
    accept_content: list[str] = ["json"]
    timezone: str = "UTC"
    enable_utc: bool = True
    result_expires: int = 60
    cpu_bound_queue_name: str = "cpu-bound"
    io_bound_queue_name: str = "io-bound"
    exchange_name: str = "tasks"

    @property
    def broker_url(self) -> str:
        """
        Build broker URL for Celery using Redis connection and broker DB index.

        Returns
        -------
        str
            Broker URL in format: redis://username:password@host:port/db_index
        """

        return f"{redis_config.connection_url}/{self.broker_db_index}"

    @property
    def result_backend_url(self) -> str:
        """
        Build result backend URL for Celery using Redis connection and result DB index.

        Returns
        -------
        str
            Result backend URL in format: redis://username:password@host:port/db_index
        """
        
        return f"{redis_config.connection_url}/{self.result_db_index}"

    @property
    def exchange_type(self) -> str:
        """
        Exchange type used for task queue routing.

        Returns
        -------
        str
            Always returns ``"direct"``.

        Notes
        -----
        This value is intentionally immutable and not configurable via environment variables.
        The entire queue routing logic — binding of ``cpu_bound_queue_name`` and
        ``io_bound_queue_name`` to a single shared exchange via their respective routing keys —
        is built on the assumption of a ``direct`` exchange.

        Changing this to ``fanout`` or ``topic`` would break routing:
        messages would be delivered to both queues simultaneously (fanout)
        or require pattern-based routing keys (topic) which are not configured here.
        """

        return "direct"


# Initialize Celery configuration singleton
# Since Celery settings are static for the application's lifetime
# and any configuration changes require a full application restart,
# it is safe to instantiate the config once at module level and reuse
# it throughout the application as a singleton.
celery_config = CeleryConfig()