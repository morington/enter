from pathlib import Path

import structlog
import yaml

from src.core.application.interfaces import RepositoryInterface
from src.core.domain.exceptions import InvalidYamlConfigurationError, AliasNotFoundError, UnknownYamlConfigurationError, \
    AliasConfigurationFileNotFound
from src.core.domain.models import Alias, Script, Argument
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.yaml.name)


class YamlRepository(RepositoryInterface):
    """
    A repository implementation that reads and parses aliases from a YAML file.

    Attributes:
        file_path (Path): The path to the YAML configuration file.

    Methods:
        __init__: Initializes the repository and validates the YAML file.
        get_all: Retrieves all aliases from the YAML file.
        get: Retrieves a specific alias by its name.
        _validate_file: Validates the existence and format of the YAML file.
        _parse_aliases: Parses aliases from the YAML data.
        _parse_arguments: Parses arguments (optional or required) from the YAML data.
    """

    def __init__(self, file_path: str):
        """
        Initializes the repository and validates the YAML file.

        Args:
            file_path (str): The path to the YAML configuration file.

        Raises:
            AliasConfigurationFileNotFound: If the YAML file does not exist.
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise AliasConfigurationFileNotFound(logger)
        else:
            logger.debug("Alias configuration file found", path=self.file_path.absolute())

        self._validate_file()

    def _validate_file(self) -> None:
        """
        Validates the existence and format of the YAML file.

        Raises:
            FileNotFoundError: If the file does not exist.
            InvalidYamlConfigurationError: If the file is not a YAML file.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Alias file {self.file_path} not found")
        if not self.file_path.suffix.lower() in ('.yaml', '.yml'):
            raise InvalidYamlConfigurationError(logger)

    def get_all(self) -> dict[str, Alias]:
        """
        Retrieves all aliases from the YAML file.

        Returns:
            dict[str, Alias]: A dictionary mapping alias names to Alias objects.

        Raises:
            InvalidYamlConfigurationError: If the YAML file is invalid.
            UnknownYamlConfigurationError: If an unknown error occurs while parsing the YAML file.
        """
        try:
            with self.file_path.open('r') as f:
                data = yaml.safe_load(f) or {}
                return self._parse_aliases(data)
        except yaml.YAMLError as e:
            raise InvalidYamlConfigurationError(logger, err=e) from e
        except Exception as e:
            raise UnknownYamlConfigurationError(logger, err=e) from e

    def get(self, alias_name: str) -> Alias:
        """
        Retrieves a specific alias by its name.

        Args:
            alias_name (str): The name of the alias to retrieve.

        Returns:
            Alias: The Alias object corresponding to the given name.

        Raises:
            AliasNotFoundError: If the alias is not found in the YAML file.
        """
        aliases = self.get_all()

        if alias_name not in aliases:
            raise AliasNotFoundError(logger)

        return aliases[alias_name]

    def _parse_aliases(self, data: dict) -> dict[str, Alias]:
        """
        Parses aliases from the YAML data.

        Args:
            data (dict): The YAML data loaded from the file.

        Returns:
            dict[str, Alias]: A dictionary mapping alias names to Alias objects.
        """
        aliases = {}

        # Parse scripts from the YAML data
        scripts = {
            name: Script(name=name, content=content)
            for name, content in data.get('scripts', {}).items()
        }

        if scripts:
            logger.debug("Loaded scripts", _count=len(scripts.keys()), scripts=list(scripts.keys()))
        else:
            logger.debug("Scripts not found")

        # Parse aliases from the YAML data
        data_aliases = data.get('aliases')
        if data_aliases:
            for alias_name, config in data_aliases.items():
                with structlog.contextvars.bound_contextvars(_ALIAS=alias_name):
                    args = self._parse_arguments(config.get('args', {}), required=False)
                    rargs = self._parse_arguments(config.get('rargs', {}), required=True)

                    logger.debug("Optional arguments received", **{name: argument.description for name, argument in args.items()})
                    logger.debug("Required arguments received", **{name: rargument.description for name, rargument in rargs.items()})

                    aliases[alias_name] = Alias(
                        name=alias_name,
                        description=config.get('description', 'No description'),
                        commands=config.get('commands', ''),
                        args={**args},
                        rargs={**rargs},
                        scripts=scripts
                    )

        if aliases:
            logger.debug("Loaded aliases", _count=len(aliases.keys()), aliases=list(aliases.keys()))
        else:
            logger.debug("Aliases not found")

        return aliases

    @staticmethod
    def _parse_arguments(arguments: dict, required: bool) -> dict[str, Argument]:
        """
        Parses arguments (optional or required) from the YAML data.

        Args:
            arguments (dict): The arguments section from the YAML data.
            required (bool): Whether the arguments are required.

        Returns:
            dict[str, Argument]: A dictionary mapping argument names to Argument objects.
        """
        return {
            name: Argument(
                name=name,
                description=details.get('description', '') if details else "Unknown",
                default=details.get('default') if details else None,
                required=required
            )
            for name, details in arguments.items()
        }