import structlog

from src.core.application.app import app
from src.core.domain.exceptions import AppCritical
from src.infrastructure.cli import CommandLineInterfaceParser
from src.infrastructure.improved_logging.loggers import InitLoggers

logger: structlog.BoundLogger = structlog.getLogger(InitLoggers.main.name)


def main() -> None:
    args = CommandLineInterfaceParser.parser()

    InitLoggers(debug=args.debug)
    logger.debug("Initializing")

    try:
        app(args)
    except Exception as e:
        from src.core.domain.exceptions import BaseError
        if not isinstance(e, BaseError):
            raise AppCritical(logger, err=e) from e


if __name__ == "__main__":
    main()
