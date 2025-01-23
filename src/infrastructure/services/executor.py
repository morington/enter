import subprocess

import structlog

from src.core.application.interfaces import CommandExecutor
from src.core.domain.exceptions import CommandExecutionError
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.executor.name)


import subprocess


class SubprocessExecutor(CommandExecutor):
    """
    A command executor implementation that uses the `subprocess` module to execute shell commands.

    Methods:
        execute: Executes a shell command using `subprocess.run`.
    """

    def execute(self, command: str) -> None:
        """
        Executes the provided shell command.

        Args:
            command (str): The shell command to execute.

        Raises:
            CommandExecutionError: If the command execution fails.
        """
        try:
            # Execute the command using subprocess.run
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            # Raise a custom error if the command fails
            raise CommandExecutionError(logger, err=e) from e