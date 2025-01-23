import structlog

from src.core.application.use_cases.execute import ExecuteAliasUseCase
from src.core.application.use_cases.list_aliases import ListAliasesUseCase
from src.core.application.use_cases.show_info_alias import ShowAliasInfoUseCase
from src.core.domain.exceptions import AppCritical
from src.infrastructure.cli import CommandLineInterfaceParser
from src.infrastructure.improved_logging.loggers import InitLoggers
from src.infrastructure.repositories.yaml_repository import YamlRepository
from src.infrastructure.services.executor import SubprocessExecutor

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.main.name)



def main() -> None:
    args = CommandLineInterfaceParser.parser()

    InitLoggers(debug=args.debug)
    logger.debug("Initializing")

    executor = SubprocessExecutor()

    try:
        repository = YamlRepository(file_path="aliases.yml")

        if args.list:
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
            print("No valid command specified")
    except Exception as e:
        from src.core.domain.exceptions import BaseError
        if not isinstance(e, BaseError):
            raise AppCritical(logger, err=e) from e


if __name__ == "__main__":
    main()
