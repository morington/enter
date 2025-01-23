from argparse import Namespace, ArgumentParser

import structlog

from src.infrastructure.improved_logging.loggers import InitLoggers
from src.core.domain.exceptions import ParserInvalidArgument


logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.cli.name)


class CommandLineInterfaceParser:
    @staticmethod
    def parser() -> Namespace:
        parser = ArgumentParser(description="Alias execution system")

        parser.add_argument("alias", nargs="?", help="Alias name to execute")
        parser.add_argument("args", nargs="*", help="Arguments for the alias")
        parser.add_argument("--debug", action="store_true", help="Enable debug mode")
        parser.add_argument("--list", action="store_true", help="List all aliases")
        parser.add_argument("--info", action="store_true", help="Show alias details")
        parser.add_argument("-c", "--commands", action="store_true", help="Show alias commands")

        return parser.parse_args()

    @staticmethod
    def parse_alias_arguments(raw_args: list) -> dict[str, str]:
        parsed = {}
        for arg in raw_args:
            if '=' not in arg:
                raise ParserInvalidArgument(logger, arg=arg)
            key, value = arg.split('=', 1)
            parsed[key.strip()] = value.strip()
        return parsed
