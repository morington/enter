from abc import ABC, abstractmethod

from src.core.domain.models import Alias


class RepositoryInterface(ABC):
    """
    An abstract base class defining the interface for a repository that manages aliases.

    Methods:
        get_all: Retrieves all aliases from the repository.
        get: Retrieves a specific alias by its name.
    """

    @abstractmethod
    def get_all(self) -> dict[str, Alias]:
        """
        Retrieves all aliases stored in the repository.

        Returns:
            dict[str, Alias]: A dictionary mapping alias names to Alias objects.
        """
        ...

    @abstractmethod
    def get(self, alias_name: str) -> Alias:
        """
        Retrieves a specific alias by its name.

        Args:
            alias_name (str): The name of the alias to retrieve.

        Returns:
            Alias: The Alias object corresponding to the given name.
        """
        ...


class CommandExecutor(ABC):
    """
    An abstract base class defining the interface for executing commands.

    Methods:
        execute: Executes a given command.
    """

    @abstractmethod
    def execute(self, command: str) -> None:
        """
        Executes the provided command.

        Args:
            command (str): The command to execute.
        """
        ...


class ConfigInterface(ABC):
    """
    An abstract base class defining the interface for accessing configuration settings.

    Methods:
        get: Retrieves a configuration value by its key.
        yaml_file_path: Retrieves the file path for the YAML configuration file.
        lang: Retrieves the language setting from the configuration.
    """

    @abstractmethod
    def get(self, key: str) -> str:
        """
        Retrieves a configuration value by its key.

        Args:
            key (str): The key for the configuration value.

        Returns:
            str: The configuration value corresponding to the key.
        """
        ...

    @abstractmethod
    def yaml_file_path(self) -> str:
        """
        Retrieves the file path for the YAML configuration file.

        Returns:
            str: The file path to the YAML configuration file.
        """
        ...

    @abstractmethod
    def lang(self) -> str:
        """
        Retrieves the language setting from the configuration.

        Returns:
            str: The language setting (e.g., "en", "ru").
        """
        ...