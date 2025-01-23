from typing import Optional

import structlog


class BaseError(Exception):
    """Базовый класс ошибок"""

    message: str = "BaseError"

    def __init__(self, logger: structlog.BoundLogger, error: bool = True, err: Optional[Exception] = None, **kwargs):
        if error:
            logger.error(self.message, _cl_err=err.__class__.__name__, _desc_err=str(err), **kwargs, exc_info=True)
        else:
            logger.info(self.message, **kwargs)

        super().__init__(self.message)


class ParserInvalidArgument(BaseError):
    message = "Invalid argument format"


class AppCritical(BaseError):
    message = "Unknown error application"


class CommandExecutionError(BaseError):
    message = "Command execution"


class AliasesListError(BaseError):
    message = "Listing aliases"


class MissingRequiredArgumentsError(BaseError):
    message = "Missing required arguments"


class InvalidConfigurationError(BaseError):
    message = "Invalid configuration"


class UnknownConfigurationError(BaseError):
    message = "Unknown error configuration"


class AliasNotFoundError(BaseError):
    message = "Alias not found"


class ShowInfoAliasError(BaseError):
    message = "Displaying alias information"


class AliasConfigurationFileNotFound(BaseError):
    message = "The alias configuration file does not exist"