import structlog

from src.core.application.interfaces import RepositoryInterface
from src.core.domain.exceptions import AliasesListError
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.cli.name)


class ListAliasesUseCase:
    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    def execute(self) -> None:
        try:
            aliases = self.repository.get_all()
            if not aliases:
                print("No aliases found")
                return

            print("[▼] Available aliases:")
            for name, alias in aliases.items():
                print(f"  › {name}: {alias.description}")
        except Exception as e:
            raise AliasesListError(logger, err=e) from e