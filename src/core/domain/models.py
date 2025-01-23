from dataclasses import dataclass
from typing import Optional

import structlog

from src.core.domain.exceptions import MissingRequiredArgumentsError
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.models.name)

from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass(frozen=True)
class Argument:
    """
    Represents an argument for an alias.

    Attributes:
        name (str): The name of the argument.
        description (str): A description of the argument.
        default (Optional[str]): The default value of the argument. Defaults to None.
        required (bool): Whether the argument is required. Defaults to False.
    """
    name: str
    description: str
    default: Optional[str] = None
    required: bool = False


@dataclass
class Script:
    """
    Represents a script associated with an alias.

    Attributes:
        name (str): The name of the script.
        content (str): The content of the script.
    """
    name: str
    content: str


@dataclass
class Alias:
    """
    Represents an alias, which includes commands, arguments, and scripts.

    Attributes:
        name (str): The name of the alias.
        description (str): A description of the alias.
        commands (str): The commands associated with the alias.
        args (Dict[str, Argument]): Optional arguments for the alias.
        rargs (Dict[str, Argument]): Required arguments for the alias.
        scripts (Dict[str, Script]): Scripts associated with the alias.

    Methods:
        combine_arguments: Combines optional and required arguments into a single list.
        validate_arguments: Validates if the provided arguments meet the alias requirements.
    """
    name: str
    description: str
    commands: str
    args: Dict[str, Argument]
    rargs: Dict[str, Argument]
    scripts: Dict[str, Script]

    def combine_arguments(self) -> List[Argument]:
        """
        Combines optional and required arguments into a single list.

        Returns:
            List[Argument]: A list of all arguments (both optional and required).
        """
        return list(self.args.values()) + list(self.rargs.values())

    def validate_arguments(self, provided_args: Dict[str, str]) -> bool:
        """
        Validates if the provided arguments meet the alias requirements.

        Args:
            provided_args (Dict[str, str]): A dictionary of provided arguments.

        Returns:
            bool: True if all required arguments are provided, otherwise False.
        """
        # Identify missing required arguments
        missing = [
            arg for arg in self.combine_arguments()
            if arg.required and not arg.default and arg.name not in provided_args
        ]

        # Print missing arguments and their descriptions
        if missing:
            print("No arguments passed:")
            for argument in missing:
                print(f"  ▣ {argument.name}* - {argument.description}")
            return False

        return True