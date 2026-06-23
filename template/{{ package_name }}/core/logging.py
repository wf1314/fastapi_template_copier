import inspect
import logging
import os
import sys
from pathlib import Path
from types import FrameType
from typing import Any

from loguru import logger

from .config import Settings, settings

TEXT_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

STANDARD_LOG_RECORD_ATTRIBUTES = frozenset(
    logging.LogRecord(
        name="",
        level=0,
        pathname="",
        lineno=0,
        msg="",
        args=(),
        exc_info=None,
    ).__dict__
)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame: FrameType | None = inspect.currentframe()
        depth = 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        extra = {
            key: value
            for key, value in record.__dict__.items()
            if key not in STANDARD_LOG_RECORD_ATTRIBUTES
        }
        logger.bind(**extra).opt(
            depth=depth,
            exception=record.exc_info,
        ).log(level, record.getMessage())


def _secure_file_opener(path: str, flags: int) -> int:
    return os.open(path, flags, 0o600)


def _sink_options(config: Settings, *, serialize: bool) -> dict[str, Any]:
    options: dict[str, Any] = {
        "level": config.LOG_LEVEL.upper(),
        "serialize": serialize,
        "enqueue": config.LOG_ENQUEUE,
        "backtrace": False,
        "diagnose": False,
    }
    if not serialize:
        options["format"] = TEXT_FORMAT
    return options


def _configure_standard_logging() -> None:
    handler = InterceptHandler()
    logging.basicConfig(handlers=[handler], level=0, force=True)
    logging.captureWarnings(True)

    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        standard_logger = logging.getLogger(logger_name)
        standard_logger.handlers.clear()
        standard_logger.setLevel(logging.NOTSET)
        standard_logger.propagate = True


def setup_logging(config: Settings | None = None) -> None:
    config = config or settings
    serialize = config.LOG_FORMAT == "json" or (
        config.LOG_FORMAT == "auto" and config.ENVIRONMENT == "prod"
    )

    logger.complete()
    logger.remove()
    logger.configure(
        extra={
            "service": config.APP_NAME,
            "environment": config.ENVIRONMENT,
        }
    )
    _configure_standard_logging()

    logger.add(
        sys.stderr,
        colorize=not serialize and sys.stderr.isatty(),
        **_sink_options(config, serialize=serialize),
    )

    if not config.LOG_FILE_ENABLED:
        return

    log_dir = Path(config.LOG_FILE_DIR)
    log_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    log_dir.chmod(0o700)

    compression = (
        None
        if config.LOG_FILE_COMPRESSION.lower() == "none"
        else config.LOG_FILE_COMPRESSION
    )
    file_options = {
        **_sink_options(config, serialize=serialize),
        "rotation": config.LOG_FILE_ROTATION,
        "retention": config.LOG_FILE_RETENTION,
        "compression": compression,
        "encoding": "utf-8",
        "opener": _secure_file_opener,
    }
    process_id = os.getpid()
    application_log = log_dir / f"application-{process_id}.log"
    error_log = log_dir / f"error-{process_id}.log"

    logger.add(application_log, **file_options)
    error_file_options = {
        key: value for key, value in file_options.items() if key != "level"
    }
    logger.add(error_log, level="ERROR", **error_file_options)

    application_log.chmod(0o600)
    error_log.chmod(0o600)
