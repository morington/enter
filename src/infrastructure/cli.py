from argparse import ArgumentParser, Namespace

import structlog

from src.infrastructure.improved_logging.loggers import InitLoggers
from src.core.domain.exceptions import ParserInvalidArgument

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.cli.name)


class CommandLineInterfaceParser:
    """
    A utility class for parsing command-line arguments and alias arguments.

    Methods:
        parser: Parses command-line arguments for the alias execution system.
        parse_alias_arguments: Parses raw alias arguments into a dictionary.
    """

    @staticmethod
    def parser() -> Namespace:
        """
        Parses command-line arguments for the alias execution system.

        Returns:
            Namespace: An object containing the parsed command-line arguments.
        """
        parser = ArgumentParser(description="Alias execution system")

        # Define command-line arguments
        parser.add_argument("alias", nargs="?", help="Alias name to execute")
        parser.add_argument("args", nargs="*", help="Arguments for the alias")
        parser.add_argument("--debug", action="store_true", help="Enable debug mode")
        parser.add_argument("--list", action="store_true", help="List all aliases")
        parser.add_argument("--info", action="store_true", help="Show alias details")
        parser.add_argument("-c", "--commands", action="store_true", help="Show alias commands")

        return parser.parse_args()

    @staticmethod
    def parse_alias_arguments(raw_args: list) -> dict[str, str]:
        """
        Parses raw alias arguments into a dictionary.

        Args:
            raw_args (list): A list of raw arguments in the format `key=value`.

        Returns:
            dict[str, str]: A dictionary of parsed arguments.

        Raises:
            ParserInvalidArgument: If an argument is not in the `key=value` format.
        """
        parsed = {}
        for arg in raw_args:
            if '=' not in arg:
                raise ParserInvalidArgument(logger, arg=arg)
            key, value = arg.split('=', 1)
            parsed[key.strip()] = value.strip()
        return parsed