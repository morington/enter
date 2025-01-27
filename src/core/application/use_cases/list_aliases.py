import structlog

from src.core.application.interfaces import RepositoryInterface
from src.core.domain.exceptions import AliasesListError
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.cli.name)


class ListAliasesUseCase:
    def __init__(self, repository: RepositoryInterface):
        """
        Инициализирует ListAliasesUseCase с помощью репозитория.

        Args:
            repository (RepositoryInterface): Репозиторий, из которого нужно получить сведения об алиасах
        """
        self.repository = repository

    def execute(self) -> None:
        """
        Выбирает и отображает все доступные алиасы из репозитория.

        Raises:
            AliasesListError: Если возникает ошибка при извлечении или перечислении алиасов
        """
        try:
            aliases = self.repository.get_all()

            if not aliases:
                print("Алиасы не найдены")
                return

            print("[▼] Доступные алиасы:")
            for name, alias in aliases.items():
                print(f"  › {name}: {alias.description}")

        except Exception as e:
            raise AliasesListError(logger, err=e) from e