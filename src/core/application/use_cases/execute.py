import re

import structlog

from src.core.application.interfaces import CommandExecutor
from src.core.domain.models import Alias
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.executor.name)


class ExecuteAliasUseCase:
    """
    A use case for executing commands based on a provided alias and arguments.

    Attributes:
        executor (CommandExecutor): An interface responsible for executing commands.
    """

    def __init__(self, executor: CommandExecutor) -> None:
        """
        Initializes the ExecuteAliasUseCase with a command executor.

        Args:
            executor (CommandExecutor): The executor used to run commands.
        """
        self.executor = executor

    def execute(
            self,
            alias: Alias,
            provided_args: dict[str, str],
            show_command: bool = False
    ) -> None:
        """
        Executes the command associated with the given alias after validating and merging arguments.

        Args:
            alias (Alias): The alias containing the command and argument definitions.
            provided_args (dict[str, str]): Arguments provided by the user.
            show_command (bool, optional): If True, prints the command before execution. Defaults to False.
        """
        is_validate = alias.validate_arguments(provided_args)

        if is_validate:
            final_args = self._merge_arguments(alias, provided_args)
            command, is_scripts = self._build_command(alias, final_args)

            if show_command and not is_scripts:
                logger.warning("Command execution display enabled")
                for cmd_line in command.splitlines():
                    cmd_line = cmd_line.strip()
                    if cmd_line:
                        print(f"\n> {cmd_line}")
                        self.executor.execute(cmd_line)
            elif show_command and is_scripts:
                logger.warning("You can not view the script in line. These functions are in development!")
                self.executor.execute(command)
            else:
                self.executor.execute(command)

    @staticmethod
    def _merge_arguments(alias: Alias, provided: dict) -> dict:
        """
        Merges default arguments from the alias with provided arguments.

        Args:
            alias (Alias): The alias containing default arguments.
            provided (dict): Arguments provided by the user.

        Returns:
            dict: A dictionary containing the merged arguments.
        """
        combination = {}

        combination.update({arg.name: arg.default for arg in alias.args.values()})
        combination.update({rarg.name: rarg.default for rarg in alias.rargs.values()})

        valid_keys = set(arg.name for arg in alias.args.values()) | set(rarg.name for rarg in alias.rargs.values())
        for key in provided:
            if key not in valid_keys:
                logger.warning("Argument is not required by the alias, but it was passed", argument=key)

        combination.update(provided)

        return combination

    @staticmethod
    def _custom_format(template, **kwargs) -> str:
        # Regular expression to search for placeholders like {key}
        pattern = re.compile(r'\{(.*?)\}')

        def replace_match(match):
            key = match.group(1)  # Retrieving the key from the placeholder
            return str(kwargs.get(key, match.group(0)))

        # Replace all placeholders in the template
        return pattern.sub(replace_match, template)

    def _build_command(self, alias: Alias, args: dict) -> tuple[str, bool]:
        """
        Constructs the final command by replacing placeholders in the alias command with provided arguments.

        Args:
            alias (Alias): The alias containing the command template.
            args (dict): The arguments to replace in the command.

        Returns:
            str: The fully constructed command.
        """
        command = alias.commands
        is_scripts = False

        for script in alias.scripts.values():
            command = command.replace(f"{{{script.name}}}", script.content)
            is_scripts = True

        return self._custom_format(command, **args), is_scripts