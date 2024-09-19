from pathlib import Path

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class _SettingsModel(BaseSettings):
    """Базовые настройки."""

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
        """Определяем приоритет использования переменных."""
        return init_settings, env_settings, file_secret_settings


class _ServiceSettings(_SettingsModel):
    """Валидация настроек из файла YAML."""

    title: str
    description: str
    host: str
    port: int
    debug: bool
    kafka_host: str
    kafka_port: int
    photo_directory: str
    tags_metadata: dict[str, str]

    def kafka_url(self) -> str:
        return f'{self.kafka_host}:{self.kafka_port}'


class Settings(_SettingsModel):
    """Настройки сервиса."""

    service: _ServiceSettings


config = Settings.from_yaml('./src/config/config.yaml')
