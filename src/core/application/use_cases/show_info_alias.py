import structlog

from src.core.application.interfaces import RepositoryInterface
from src.core.domain.exceptions import ShowInfoAliasError
from src.core.domain.models import Alias
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.cli.name)


class ShowAliasInfoUseCase:
    def __init__(self, repository: RepositoryInterface) -> None:
        """
        Инициализирует ShowAliasInfoUseCase с репозиторием.

        Args:
            repository (RepositoryInterface): Репозиторий, из которого нужно получить сведения об алиасах
        """
        self.repository = repository

    def execute(self, alias_name: str, show_commands: bool = False) -> None:
        """
        Извлекает и отображает подробную информацию об указанном псевдониме.

        Args:
            alias_name (str): Имя алиаса
            show_commands (bool, False): Выводит информацию о командах алиаса, если True

        Raises:
            ShowInfoAliasError: возникает, если не удалось извлечь информацию об алиасе
        """
        try:
            alias = self.repository.get(alias_name)
            self._display_info(alias, show_commands)
        except Exception as e:
            raise ShowInfoAliasError(logger, err=e) from e

    @staticmethod
    def _display_info(alias: Alias, show_commands: bool) -> None:
        """
        Отображает подробную информацию об алиасе, включая его описание, аргументы и, при необходимости, команды.

        Args:
            alias (Alias): Объект алиаса, содержащий детали для отображения
            show_commands (bool): Выводит информацию о командах алиаса, если True
        """
        # Warn if the alias has no commands
        if not alias.commands:
            logger.warning("The alias has no commands, although the key is specified", alias=alias.name)

        print(f"Alias: {alias.name}")
        print(f"Description:\n  {alias.description}")

        if alias.args:
            print("\n[▼] Arguments:")
            for arg in alias.args.values():
                is_requiring = arg.required or not arg.default
                default = f" [ {arg.default} ]" if arg.default else ""
                icon_required = "▣" if is_requiring else "▢"
                print(f"  {icon_required} {arg.name}{'*' if is_requiring else ''}{default} - {arg.description}")

        if alias.rargs:
            print("\n[▼] Required Arguments:")
            for rarg in alias.rargs.values():
                is_requiring = rarg.required and not rarg.default
                default = f" [ {rarg.default} ]" if rarg.default else ""
                icon_required = "▣" if is_requiring else "▢"
                print(f"  {icon_required} {rarg.name}{'*' if is_requiring else ''}{default} - {rarg.description}")

        if show_commands:
            if alias.commands:
                print("\n[▼] Commands:")
                for command in alias.commands.split("\n"):
                    if command.strip():
                        print(f"  › {command}")