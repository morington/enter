import structlog

from src.core.application.app import app
from src.core.domain.exceptions import AppCritical
from src.infrastructure.cli import CommandLineInterfaceParser
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.main.name)


def main() -> None:
    """
    The main entry point of the application.

    This function initializes the application, parses command-line arguments,
    sets up logging, and delegates control to the `app` function.

    Raises:
        AppCritical: If an unexpected error occurs during execution.
    """
    # Parse command-line arguments
    args = CommandLineInterfaceParser.parser()

    # Initialize loggers with debug mode if enabled
    InitLoggers(debug=args.debug)
    logger.debug("Initializing")

    try:
        # Delegate control to the `app` function
        app(args)
    except Exception as e:
        # Handle unexpected errors
        from src.core.domain.exceptions import BaseError
        if not isinstance(e, BaseError):
            raise AppCritical(logger, err=e) from e


if __name__ == "__main__":
    # Entry point for the script
    main()
