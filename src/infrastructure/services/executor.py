import subprocess

import structlog

from src.core.application.interfaces import CommandExecutor
from src.core.domain.exceptions import CommandExecutionError
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.executor.name)


class SubprocessExecutor(CommandExecutor):
    def execute(self, command: str) -> None:
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            raise CommandExecutionError(logger, err=e) from e