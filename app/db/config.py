# app/db/config.py
from typing import ClassVar
from pydantic import Field
from ..shared import BaseConfig


class RedisConfig(BaseConfig):
    """
    Configuration schema for Redis service.

    Attributes
    ----------
    host : str
        Hostname or IP address of the Redis server. Default is `"127.0.0.1"`.
    external_port : int
        TCP port the server listens on. Must be in the range 1-65535.
        Default is `6379`.
    user_name : str
        Username for Redis authentication.
    user_password : str
        Password for Redis authentication.
    """

    env_prefix: ClassVar[str] = "REDIS_"

    host: str = "127.0.0.1"
    external_port: int = Field(default=6379, ge=1, le=65535)
    user_name: str
    user_password: str

    @property
    def connection_url(self) -> str:
        """
        Build Redis connection URL from configuration settings.

        Returns
        -------
        str
            Complete Redis connection URL with credentials
            in the format: redis://username:password@host:port
        """
        return (
            f"redis://{self.user_name}:"
            f"{self.user_password}@"
            f"{self.host}:{self.external_port}"
        )


# Initialize Redis configuration singleton
# Since Redis server settings are static for the application's lifetime
# and any configuration changes require a full application restart,
# it is safe to instantiate the config once at module level and reuse
# it throughout the application as a singleton.
redis_config = RedisConfig()