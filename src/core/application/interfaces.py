from abc import ABC, abstractmethod

from src.core.domain.models import Alias


class RepositoryInterface(ABC):
    """
    Абстрактный базовый класс, определяющий интерфейс репозитория, управляющего чтением алиасов.

    Methods:
        get_all: Получает все алиасы из репозитория
        get: Получает определенный алиас по его имени
    """

    @abstractmethod
    def get_all(self) -> dict[str, Alias]:
        """
        Получает все алиасы из репозитория.

        Returns:
            dict[str, Alias]: Карта имен алиасов и объектов
        """
        ...

    @abstractmethod
    def get(self, alias_name: str) -> Alias:
        """
        Получает определенный алиас по его имени.

        Args:
            alias_name (str): Имя алиаса

        Returns:
            Alias: Объект Алиаса
        """
        ...


class CommandExecutor(ABC):
    """
    Абстрактный базовый класс, определяющий интерфейс для выполнения команд.

    Methods:
        execute: Выполняет заданную команду
    """

    @abstractmethod
    def execute(self, command: str) -> None:
        """
        Выполняет заданную команду.

        Args:
            command (str): Команда для выполнения
        """
        ...


class ConfigInterface(ABC):
    """
    Абстрактный базовый класс, определяющий интерфейс доступа к настройкам конфигурации.

    Methods:
        get: Получает значение конфигурации по своему ключу
        home_path: Отдает путь к проекту
        aliases_path: Отдает путь к файлу алиасов
    """

    @abstractmethod
    def get(self, key: str) -> str:
        """
        Получает значение конфигурации по своему ключу.

        Args:
            key (str): Ключ

        Returns:
            str: Значение из конфигурации. В основном отдается строка.
        """
        ...

    @abstractmethod
    def home_path(self) -> str:
        """
        home_path: Отдает путь к проекту

        Returns:
            str: Путь
        """
        ...

    @abstractmethod
    def aliases_path(self) -> str:
        """
        Отдает путь к файлу алиасов.

        Returns:
            str: Путь к файлу
        """
        ...