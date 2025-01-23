import structlog

from src.core.application.interfaces import RepositoryInterface
from src.core.domain.exceptions import AliasesListError
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.cli.name)


class ListAliasesUseCase:
    """
    A use case for listing all available aliases from a repository.

    Attributes:
        repository (RepositoryInterface): The repository interface used to fetch aliases.
    """

    def __init__(self, repository: RepositoryInterface):
        """
        Initializes the ListAliasesUseCase with a repository.

        Args:
            repository (RepositoryInterface): The repository to fetch aliases from.
        """
        self.repository = repository

    def execute(self) -> None:
        """
        Fetches and displays all available aliases from the repository.

        Raises:
            AliasesListError: If an error occurs while fetching or listing aliases.
        """
        try:
            # Fetch all aliases from the repository
            aliases = self.repository.get_all()

            # Handle case where no aliases are found
            if not aliases:
                print("No aliases found")
                return

            # Display available aliases
            print("[▼] Available aliases:")
            for name, alias in aliases.items():
                print(f"  › {name}: {alias.description}")

        except Exception as e:
            # Raise a custom error with logging
            raise AliasesListError(logger, err=e) from e