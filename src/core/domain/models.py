from dataclasses import dataclass
from typing import Optional

import structlog

from src.core.domain.exceptions import MissingRequiredArgumentsError
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.models.name)

@dataclass(frozen=True)
class Argument:
    name: str
    description: str
    default: Optional[str] = None
    required: bool = False

@dataclass
class Script:
    name: str
    content: str

@dataclass
class Alias:
    name: str
    description: str
    commands: str
    args: dict[str, Argument]
    rargs: dict[str, Argument]
    scripts: dict[str, Script]

    def combine_arguments(self) -> list[Argument]:
        return list(self.args.values()) + list(self.rargs.values())

    def validate_arguments(self, provided_args: dict[str, str]) -> bool:
        missing = [
            arg for arg in self.combine_arguments()
            if arg.required and not arg.default and arg.name not in provided_args
        ]
        if missing:
            print("No arguments passed:")
            for argument in missing:
                print(f"  ▣ {argument.name}* - {argument.description}")
            return False
        return True