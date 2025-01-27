import re

import structlog

from src.core.application.interfaces import CommandExecutor
from src.core.domain.models import Alias
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.executor.name)


class ExecuteAliasUseCase:
    def __init__(self, executor: CommandExecutor) -> None:
        """
        Инициализирует ExecuteAliasUseCase с помощью исполнителя команд.

        Args:
            executor (CommandExecutor): Исполнитель, используемый для запуска команд.
        """
        self.executor = executor

    def execute(
            self,
            alias: Alias,
            provided_args: dict[str, str],
            show_command: bool = False
    ) -> None:
        """
        Выполняет команду, связанную с данным алиасов, после проверки и объединения аргументов.

        Args:
            alias (Alias): Объект Алиас, содержащий определения команды и аргументов
            provided_args (dict[str, str]): Аргументы, предоставленные пользователем
            show_command (bool, optional): Предоставляет информацию о выполнениях команд алиаса, если True
        """
        is_validate = alias.validate_arguments(provided_args)

        if is_validate:
            final_args = self._merge_arguments(alias, provided_args)
            command, is_scripts = self._build_command(alias, final_args)

            if show_command and not is_scripts:
                logger.warning("Отображение выполнения команды включено")
                for cmd_line in command.splitlines():
                    cmd_line = cmd_line.strip()
                    if cmd_line:
                        print(f"\n> {cmd_line}")
                        self.executor.execute(cmd_line)
            elif show_command and is_scripts:
                logger.warning("Вы не можете просмотреть скрипт в режиме просмотра команд. Эти функции находятся в разработке!")
                self.executor.execute(command)
            else:
                self.executor.execute(command)

    @staticmethod
    def _merge_arguments(alias: Alias, provided: dict) -> dict:
        """
        Комбинирует обязательные и необязательные аргументы алиаса в один словарь

        Args:
            alias (Alias): Объект Алиас, содержащий аргументы
            provided (dict): Аргументы, предоставленные пользователем

        Returns:
            dict: Комбинированный словарь аргументов
        """
        combination = {}

        combination.update({arg.name: arg.default for arg in alias.args.values()})
        combination.update({rarg.name: rarg.default for rarg in alias.rargs.values()})

        valid_keys = set(arg.name for arg in alias.args.values()) | set(rarg.name for rarg in alias.rargs.values())
        for key in provided:
            if key not in valid_keys:
                logger.warning("Аргумент был передан алиасу, но он не был задан в алиасе", argument=key)

        combination.update(provided)

        return combination

    @staticmethod
    def _custom_format(command: str, **kwargs) -> str:
        """
        Из-за сложной обработки bash сценариев, был введен кастомный форматер команд.

        Args:
            command (str): Объект Алиас, содержащий аргументы
            **kwargs (dict): Аргументы

        Returns:
            str: Форматированная команда с аргументами пользователя
        """
        pattern = re.compile(r'\{(.*?)\}')

        def replace_match(match):
            key = match.group(1)
            return str(kwargs.get(key, match.group(0)))

        return pattern.sub(replace_match, command)

    def _build_command(self, alias: Alias, args: dict) -> tuple[str, bool]:
        """
        Создает окончательную команду, подставляет аргументы в команды алиаса.

        Args:
            alias (Alias): Объект Алиас, содержащий команды
            args (dict): Аргументы пользователя

        Returns:
            tuple[str, bool]: Возвращает форматированную команду, а также проверку на скрипт
        """
        command = alias.commands
        is_scripts = False

        for script in alias.scripts.values():
            command = command.replace(f"{{{script.name}}}", script.content)
            is_scripts = True

        return self._custom_format(command, **args), is_scripts