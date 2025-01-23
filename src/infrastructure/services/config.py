import configparser
import os
from pathlib import Path

import structlog

from src.core.application.interfaces import ConfigInterface
from src.core.domain.exceptions import ConfigHandlerError
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.main.name)


class ConfigHandler(ConfigInterface):
    """
    A class for handling configuration files in INI format.

    This class is responsible for loading, validating, and retrieving values from a configuration file.
    If the configuration file does not exist, it creates one with default required fields.

    Attributes:
        _config_file (Path): Path to the configuration file. Defaults to "config.ini" in the PYTHONPATH directory.
        _required_fields (tuple[str, ...]): A tuple of required fields that must be present in the configuration file.
        _config (configparser.ConfigParser): An instance of ConfigParser for reading and writing the configuration file.
    """

    _config_file: Path = Path(os.getenv("PYTHONPATH")) / "config.ini"
    _required_fields: tuple[str, ...] = ("yaml_file_path", "lang")

    def __init__(self) -> None:
        """
        Initializes the ConfigHandler instance.

        Loads and validates the configuration file. If the file does not exist, it creates a default one.
        """
        self._config = configparser.ConfigParser()
        self._ensure_config_file_exists()
        self._load_config()
        self._validate_config()

    def _ensure_config_file_exists(self) -> None:
        """
        Ensures the configuration file exists.

        If the file does not exist, it creates a default configuration file with empty required fields.
        """
        if not self._config_file.exists():
            self._create_default_config()

    def _create_default_config(self) -> None:
        """
        Creates a default configuration file with empty required fields.

        The file is created at the path specified by `_config_file`.
        """
        self._config["ENTER"] = {field: "" for field in self._required_fields}

        with self._config_file.open("w") as file:
            self._config.write(file)  # type: ignore
            # https://youtrack.jetbrains.com/issue/PY-76945

    def _load_config(self) -> None:
        """
        Loads the configuration file into the `_config` attribute.
        """
        self._config.read(self._config_file)

    def _validate_config(self) -> None:
        """
        Validates the configuration file.

        Ensures that all required fields are present in the configuration file.
        Raises `ConfigHandlerError` if any required field is missing.
        """
        if not self._config.has_section("ENTER"):
            raise ConfigHandlerError(logger, path=self._config_file.absolute())
        for field in self._required_fields:
            if not self._config.has_option("ENTER", field):
                raise ConfigHandlerError(logger, path=self._config_file.absolute())

    def get(self, key: str) -> str:
        """
        Retrieves the value of a specified key from the configuration file.

        Args:
            key (str): The key whose value needs to be retrieved.

        Returns:
            str: The value associated with the key.

        Raises:
            ConfigHandlerError: If the value is empty or the key is not found.
        """
        value = self._config.get("ENTER", key)
        if not value.strip():
            raise ConfigHandlerError(logger, path=self._config_file.absolute())
        return value

    @property
    def yaml_file_path(self) -> Path:
        """
        Retrieves the path to the YAML file from the configuration.

        Returns:
            Path: The path to the YAML file.
        """
        return Path(self.get("yaml_file_path"))

    @property
    def lang(self) -> str:
        """
        Retrieves the language setting from the configuration.

        Returns:
            str: The language specified in the configuration.
        """
        return self.get("lang")