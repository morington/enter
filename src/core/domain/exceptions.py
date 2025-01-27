from typing import Optional

import structlog


class BaseError(Exception):
    """
    A base exception class for custom errors in the application.

    Attributes:
        message (str): The default error message.
    """

    message: str = "BaseError"

    def __init__(
        self,
        logger: structlog.BoundLogger,
        error: bool = True,
        err: Optional[Exception] = None,
        **kwargs
    ):
        """
        Initializes the error and logs it using the provided logger.

        Args:
            logger (structlog.BoundLogger): The logger instance for logging the error.
            error (bool, optional): If True, logs the error as an error-level message. Defaults to True.
            err (Optional[Exception], optional): The original exception that caused the error. Defaults to None.
            **kwargs: Additional context to include in the log message.
        """
        if error:
            err_kwargs = {
                "_cl_err": err.__class__.__name__ if err else None,
                "_desc_err": str(err) if err else None
            }

            logger.error(
                self.message,
                **err_kwargs if err else {},
                **kwargs,
                exc_info=True
            )
        else:
            logger.info(self.message, **kwargs)

        super().__init__(self.message)


class ConfigHandlerError(BaseError):
    """Raised when there is an issue with the configuration file."""
    message = "Invalid configuration file"


class ParserInvalidArgument(BaseError):
    """Raised when an invalid argument format is encountered."""
    message = "Invalid argument format"


class AppCritical(BaseError):
    """Raised for unknown critical errors in the application."""
    message = "Unknown error application"


class CommandExecutionError(BaseError):
    """Raised when a command execution fails."""
    message = "Command execution"


class AliasesListError(BaseError):
    """Raised when there is an error while listing aliases."""
    message = "Listing aliases"


class MissingRequiredArgumentsError(BaseError):
    """Raised when required arguments are missing."""
    message = "Missing required arguments"


class InvalidYamlConfigurationError(BaseError):
    """Raised when the YAML configuration is invalid."""
    message = "Invalid yaml configuration"


class UnknownYamlConfigurationError(BaseError):
    """Raised for unknown errors related to YAML configuration."""
    message = "Unknown error yaml configuration"


class AliasNotFoundError(BaseError):
    """Raised when a requested alias is not found."""
    message = "Alias not found"


class ShowInfoAliasError(BaseError):
    """Повышен при ошибке при отображении информации о псевдониме."""
    message = "Displaying alias information"


class AliasConfigurationFileNotFound(BaseError):
    """Возникает, когда файл конфигурации не существует."""
    message = "Файл конфигурации проекта не найден"