from pathlib import Path

import yaml
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class _SettingsModel(BaseSettings):
    """Base settings."""

    @classmethod
    def from_yaml(cls, config_path: str) -> '_SettingsModel':
        return cls(
            **yaml.safe_load(Path(config_path).read_text(encoding='utf-8')),
        )

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix='EMP_',
        env_nested_delimiter='__',
    )

    @classmethod
    def customise_sources(
        cls,
        init_settings,
        env_settings,
        file_secret_settings,
    ):
        """Variables priority."""
        return init_settings, env_settings, file_secret_settings


class _ServiceSettings(_SettingsModel):
    """Service settings validation."""

    title: str
    description: str
    host: str
    port: int
    debug: bool
    kafka_host: str
    kafka_port: int
    kafka_topic: str
    photo_directory: str
    db_hostname: str
    db_port: int
    db_name: str
    db_username: str
    db_echo: bool

    @property
    def kafka_url(self) -> str:
        return f'{self.kafka_host}:{self.kafka_port}'


class _SettingsSecret(BaseSettings):
    """Secret settings validation."""

    db_password: SecretStr = SecretStr('password')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )


class Settings(_SettingsModel, _SettingsSecret):
    """Service settings."""

    service: _ServiceSettings

    @property
    def database_url(self):
        """Database async link."""
        return (
            f'postgresql+asyncpg://{self.service.db_username}:'
            f'{self.db_password.get_secret_value()}@'
            f'{self.service.db_hostname}:'
            f'{self.service.db_port}/{self.service.db_name}'
        )

    @property
    def sync_database_url(self):
        """Database sync link."""
        return (
            f'postgresql://{self.service.db_username}:'
            f'{self.db_password.get_secret_value()}@'
            f'{self.service.db_hostname}:'
            f'{self.service.db_port}/{self.service.db_name}'
        )


config = Settings.from_yaml('./src/config/config.yaml')
