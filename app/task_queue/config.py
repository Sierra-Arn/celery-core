# app/task_queue/config.py
from typing import ClassVar
from pydantic import Field
from .shared import BaseConfig


class CeleryConfig(BaseConfig):
    """
    Configuration schema for Celery task queue service.

    Attributes
    ----------
    redis_host : str
        Hostname or IP address of the Redis server. Default is "127.0.0.1".
    redis_external_port : int
        TCP port the Redis server listens on. Must be in range 1-65535. Default is 6379.
    redis_username : str
        Username for Redis authentication.
    redis_password : str
        Password for Redis authentication.
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
    cpu_bound_queue_max_priority : int
        Maximum priority level for the CPU-bound queue. Lower numbers mean higher priority. Default is 5.
    io_bound_queue_name : str
        Name of the queue for I/O-intensive tasks. Default is "io-bound".
    io_bound_queue_max_priority : int
        Maximum priority level for the I/O-bound queue. Lower numbers mean higher priority. Default is 3.

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

    redis_host: str = "127.0.0.1"
    redis_external_port: int = Field(default=6379, ge=1, le=65535)
    redis_username: str
    redis_password: str
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
    cpu_bound_queue_max_priority: int = 5
    io_bound_queue_name: str = "io-bound"
    io_bound_queue_max_priority: int = 3

    @property
    def redis_connection_url(self) -> str:
        """
        Build Redis connection URL from configuration settings.

        Returns
        -------
        str
            Complete Redis connection URL with credentials
            in the format: redis://username:password@host:port
        """
        return (
            f"redis://{self.redis_username}:"
            f"{self.redis_password}@"
            f"{self.redis_host}:{self.redis_external_port}"
        )

    @property
    def broker_url(self) -> str:
        """
        Build broker URL for Celery using Redis connection and broker DB index.

        Returns
        -------
        str
            Broker URL in format: redis://username:password@host:port/db_index
        """
        return f"{self.redis_connection_url}/{self.broker_db_index}"

    @property
    def result_backend_url(self) -> str:
        """
        Build result backend URL for Celery using Redis connection and result DB index.

        Returns
        -------
        str
            Result backend URL in format: redis://username:password@host:port/db_index
        """
        return f"{self.redis_connection_url}/{self.result_db_index}"


# Initialize Celery configuration singleton
# Since Celery settings are static for the application's lifetime
# and any configuration changes require a full application restart,
# it is safe to instantiate the config once at module level and reuse
# it throughout the application as a singleton.
celery_config = CeleryConfig()