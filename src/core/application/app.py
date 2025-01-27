from argparse import Namespace

from src.core.application.use_cases.execute import ExecuteAliasUseCase
from src.core.application.use_cases.list_aliases import ListAliasesUseCase
from src.core.application.use_cases.show_info_alias import ShowAliasInfoUseCase
from src.infrastructure.cli import CommandLineInterfaceParser
from src.infrastructure.repositories.yaml_repository import YamlRepository
from src.infrastructure.services.config import ConfigHandler
from src.infrastructure.services.executor import SubprocessExecutor


def app(args: Namespace) -> None:
    """
    Основная функция приложения, которая обрабатывает аргументы командной
    строки и делегирует задачи соответствующим вариантам использования.

    Args:
        args (Namespace): Аргументы переданные пользователем, спарсенные argparse
    """
    config = ConfigHandler()
    executor = SubprocessExecutor()

    repository = YamlRepository(file_path=config.yaml_file_path)

    if args.update:
        executor.execute("git pull", cwd=config.enter_path)

    elif args.list:
        use_case = ListAliasesUseCase(repository=repository)
        use_case.execute()

    elif args.info:
        if args.alias:
            use_case = ShowAliasInfoUseCase(repository=repository)
            use_case.execute(args.alias, args.commands)

    elif args.alias:
        use_case = ExecuteAliasUseCase(executor)
        alias = repository.get(args.alias)
        parsed_args = CommandLineInterfaceParser.parse_alias_arguments(args.args)
        use_case.execute(alias, parsed_args, show_command=args.commands)

    else:
        print("Не указана допустимая команда")