import structlog

from src.core.application.interfaces import RepositoryInterface
from src.core.domain.exceptions import ShowInfoAliasError
from src.core.domain.models import Alias
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.cli.name)


class ShowAliasInfoUseCase:
    """
    A use case for displaying detailed information about a specific alias.

    Attributes:
        repository (RepositoryInterface): The repository interface used to fetch alias details.
    """

    def __init__(self, repository: RepositoryInterface) -> None:
        """
        Initializes the ShowAliasInfoUseCase with a repository.

        Args:
            repository (RepositoryInterface): The repository to fetch alias details from.
        """
        self.repository = repository

    def execute(self, alias_name: str, show_commands: bool = False) -> None:
        """
        Fetches and displays detailed information about the specified alias.

        Args:
            alias_name (str): The name of the alias to display information for.
            show_commands (bool, optional): If True, displays the commands associated with the alias. Defaults to False.

        Raises:
            ShowInfoAliasError: If an error occurs while fetching or displaying alias information.
        """
        try:
            # Fetch the alias from the repository
            alias = self.repository.get(alias_name)
            # Display the alias information
            self._display_info(alias, show_commands)
        except Exception as e:
            # Raise a custom error with logging
            raise ShowInfoAliasError(logger, err=e) from e

    @staticmethod
    def _display_info(alias: Alias, show_commands: bool) -> None:
        """
        Displays detailed information about the alias, including its description, arguments, and optionally its commands.

        Args:
            alias (Alias): The alias object containing the details to display.
            show_commands (bool): If True, displays the commands associated with the alias.
        """
        # Warn if the alias has no commands
        if not alias.commands:
            logger.warning("The alias has no commands, although the key is specified", alias=alias.name)

        # Display alias name and description
        print(f"Alias: {alias.name}")
        print(f"Description:\n  {alias.description}")

        # Display optional arguments
        if alias.args:
            print("\n[▼] Arguments:")
            for arg in alias.args.values():
                is_requiring = arg.required or not arg.default
                default = f" [ {arg.default} ]" if arg.default else ""
                icon_required = "▣" if is_requiring else "▢"
                print(f"  {icon_required} {arg.name}{'*' if is_requiring else ''}{default} - {arg.description}")

        # Display required arguments
        if alias.rargs:
            print("\n[▼] Required Arguments:")
            for rarg in alias.rargs.values():
                is_requiring = rarg.required and not rarg.default
                default = f" [ {rarg.default} ]" if rarg.default else ""
                icon_required = "▣" if is_requiring else "▢"
                print(f"  {icon_required} {rarg.name}{'*' if is_requiring else ''}{default} - {rarg.description}")

        # Display commands if requested
        if show_commands:
            if alias.commands:
                print("\n[▼] Commands:")
                for command in alias.commands.split("\n"):
                    if command.strip():
                        print(f"  › {command}")