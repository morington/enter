from pathlib import Path
from typing import Optional

import structlog
import yaml

from src.core.application.interfaces import RepositoryInterface
from src.core.domain.exceptions import InvalidConfigurationError, AliasNotFoundError, UnknownConfigurationError, \
    AliasConfigurationFileNotFound
from src.core.domain.models import Alias, Script, Argument
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.yaml.name)


class YamlRepository(RepositoryInterface):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise AliasConfigurationFileNotFound(logger)
        else:
            logger.debug("Alias configuration file found", path=self.file_path.absolute())

        self._validate_file()

    def _validate_file(self) -> None:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Alias file {self.file_path} not found")
        if not self.file_path.suffix.lower() in ('.yaml', '.yml'):
            raise InvalidConfigurationError(logger)

    def get_all(self) -> dict[str, Alias]:
        try:
            with self.file_path.open('r') as f:
                data = yaml.safe_load(f) or {}
                return self._parse_aliases(data)
        except yaml.YAMLError as e:
            raise InvalidConfigurationError(logger, err=e) from e
        except Exception as e:
            raise UnknownConfigurationError(logger, err=e) from e

    def get(self, alias_name: str) -> Alias:
        aliases = self.get_all()

        if alias_name not in aliases:
            raise AliasNotFoundError(logger)

        return aliases[alias_name]

    def _parse_aliases(self, data: dict) -> dict[str, Alias]:
        aliases = {}

        scripts = {
            name: Script(name=name, content=content)
            for name, content in data.get('scripts', {}).items()
        }

        if scripts:
            logger.debug("Loaded scripts", _count=len(scripts.keys()), scripts=list(scripts.keys()))
        else:
            logger.debug("Scripts not found")

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
        return {
            name: Argument(
                name=name,
                description=details.get('description', '') if details else "Unknown",
                default=details.get('default') if details else None,
                required=required
            )
            for name, details in arguments.items()
        }