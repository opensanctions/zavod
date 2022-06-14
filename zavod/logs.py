import sys
import logging
import structlog
from typing import List
from structlog.stdlib import get_logger as get_raw_logger
from structlog.contextvars import merge_contextvars
from structlog.types import Processor


def configure_logging(
    level: int = logging.DEBUG,
    extra_processors: List[Processor] = [],
) -> None:
    """Configure log levels and structured logging."""
    processors: List[Processor] = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        merge_contextvars,
    ]
    processors.extend(extra_processors)
    renderer = structlog.dev.ConsoleRenderer(
        exception_formatter=structlog.dev.plain_traceback
    )
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=list(processors),
        processor=renderer,
    )

    processors.append(structlog.stdlib.ProcessorFormatter.wrap_for_formatter)

    # configuration for structlog based loggers
    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return get_raw_logger(name)
