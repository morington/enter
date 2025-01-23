import configparser
import os

import structlog

from src.core.application.interfaces import ConfigInterface
from src.core.domain.exceptions import ConfigHandlerError
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.main.name)


class ConfigHandler(ConfigInterface):
    _config_file: str = "config.ini"
    _required_fields: tuple[str, ...] = ("yaml_file_path", "lang")

    def __init__(self) -> None:
        """Инициализирует экземпляр, загружает и валидирует конфигурационный файл."""
        self._config = configparser.ConfigParser()
        self._ensure_config_file_exists()
        self._load_config()
        self._validate_config()

    def _ensure_config_file_exists(self) -> None:
        """Checks the existence of a configuration file, creates it if it does not exist."""
        if not os.path.exists(self._config_file):
            self._create_default_config()

    def _create_default_config(self) -> None:
        """Creates a configuration file with empty required fields."""
        self._config["ENTER"] = {field: "" for field in self._required_fields}

        with open(self._config_file, "w") as file:
            self._config.write(file)  # type: ignore
            # https://youtrack.jetbrains.com/issue/PY-76945

    def _load_config(self) -> None:
        """Загружает конфигурационный файл."""
        self._config.read(self._config_file)

    def _validate_config(self) -> None:
        """Проверяет наличие всех обязательных полей в конфигурации."""
        if not self._config.has_section("ENTER"):
            raise ConfigHandlerError(logger)
        for field in self._required_fields:
            if not self._config.has_option("ENTER", field):
                raise ConfigHandlerError(logger)

    def get(self, key: str) -> str:
        """Returns the value of the specified key from the configuration."""
        value = self._config.get("ENTER", key)
        if not value.strip():
            raise ConfigHandlerError(logger)
        return value

    @property
    def yaml_file_path(self) -> str:
        """Returns the path to the YAML file from the configuration."""
        return self.get("yaml_file_path")

    @property
    def lang(self) -> str:
        """Returns the language from the configuration."""
        return self.get("lang")


if __name__ == "__main__":
    try:
        config = ConfigHandler()
        print(f"YAML Path: {config.yaml_file_path}")
        print(f"Language: {config.lang}")
    except ConfigHandlerError as e:
        print(f"Configuration error: {e}")