from abc import ABC, abstractmethod

from src.core.domain.models import Alias


class RepositoryInterface(ABC):
    @abstractmethod
    def get_all(self) -> dict[str, Alias]:
        ...

    @abstractmethod
    def get(self, alias_name: str) -> Alias:
        ...



class CommandExecutor(ABC):
    @abstractmethod
    def execute(self, command: str) -> None:
        ...


class ConfigInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> str:
        ...

    @abstractmethod
    def yaml_file_path(self) -> str:
        ...

    @abstractmethod
    def lang(self) -> str:
        ...