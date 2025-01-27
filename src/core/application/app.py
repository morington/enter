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
    The main application function that handles command-line arguments and delegates tasks to appropriate use cases.

    Args:
        args (Namespace): Parsed command-line arguments.
    """
    # Initialize configuration handler and command executor
    config = ConfigHandler()
    executor = SubprocessExecutor()

    # Initialize the repository to fetch aliases from a YAML file
    repository = YamlRepository(file_path=config.yaml_file_path)

    # Process the “updates” command to update Enter.
    if args.update:
        executor.execute("git pull", cwd=config.enter_path)

    # Handle the 'list' command to display all aliases
    elif args.list:
        use_case = ListAliasesUseCase(repository=repository)
        use_case.execute()

    # Handle the 'info' command to display details about a specific alias
    elif args.info:
        if args.alias:
            use_case = ShowAliasInfoUseCase(repository=repository)
            use_case.execute(args.alias, args.commands)

    # Handle the 'alias' command to execute a specific alias with provided arguments
    elif args.alias:
        use_case = ExecuteAliasUseCase(executor)
        alias = repository.get(args.alias)
        parsed_args = CommandLineInterfaceParser.parse_alias_arguments(args.args)
        use_case.execute(alias, parsed_args, show_command=args.commands)

    # Handle invalid or missing commands
    else:
        print("No valid command specified")