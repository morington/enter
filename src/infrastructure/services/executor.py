import subprocess
from pathlib import Path
from typing import Optional

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

    def execute(self, command: str, bash: bool = True, cwd: Optional[str | Path] = None) -> None:
        """
        Executes the provided shell command.

        Args:
            bash (bool): Execution through bash
            command (str): The shell command to execute.
            cwd (Optional[str]): The path to execute the command

        Raises:
            CommandExecutionError: If the command execution fails.
        """
        try:
            # Execute the command using subprocess.run
            _command = ["/bin/bash", "-c", command] if bash else command
            subprocess.run(_command, cwd=cwd, check=True, shell=not bash)
        except subprocess.CalledProcessError as e:
            # Raise a custom error if the command fails
            raise CommandExecutionError(logger, err=e) from e