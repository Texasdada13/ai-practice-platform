"""
Logging configuration for AI Practice Platform.

Provides structured logging with different handlers for development and production.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from typing import Optional


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured log output."""

    def format(self, record: logging.LogRecord) -> str:
        # Add extra fields if available
        extra_fields = ""
        if hasattr(record, 'user_id'):
            extra_fields += f" user_id={record.user_id}"
        if hasattr(record, 'assessment_id'):
            extra_fields += f" assessment_id={record.assessment_id}"
        if hasattr(record, 'request_id'):
            extra_fields += f" request_id={record.request_id}"
        if hasattr(record, 'duration_ms'):
            extra_fields += f" duration_ms={record.duration_ms}"

        record.extra_fields = extra_fields
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """JSON formatter for production logging."""

    def format(self, record: logging.LogRecord) -> str:
        import json

        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # Add extra fields
        for key in ['user_id', 'assessment_id', 'request_id', 'duration_ms', 'ip_address']:
            if hasattr(record, key):
                log_data[key] = getattr(record, key)

        return json.dumps(log_data)


def setup_logging(
    app_name: str = 'ai_practice_platform',
    log_level: str = 'INFO',
    log_dir: Optional[str] = None,
    json_format: bool = False
) -> logging.Logger:
    """
    Set up application logging.

    Args:
        app_name: Application name for the logger
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (optional)
        json_format: Use JSON format for production

    Returns:
        Configured root logger
    """
    # Get numeric log level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create logger
    logger = logging.getLogger(app_name)
    logger.setLevel(numeric_level)
    logger.handlers = []  # Clear existing handlers

    # Choose formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = StructuredFormatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s%(extra_fields)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    # Console handler (always)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if log_dir specified)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

        # Main log file with rotation
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, f'{app_name}.log'),
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Error log file (errors and above only)
        error_handler = RotatingFileHandler(
            os.path.join(log_dir, f'{app_name}_error.log'),
            maxBytes=10 * 1024 * 1024,
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)

    return logger


def get_request_logger(logger: logging.Logger, request_id: str = None, user_id: str = None):
    """
    Get a logger adapter with request context.

    Args:
        logger: Base logger
        request_id: Request ID for tracing
        user_id: User/session ID

    Returns:
        LoggerAdapter with context
    """
    extra = {}
    if request_id:
        extra['request_id'] = request_id
    if user_id:
        extra['user_id'] = user_id

    return logging.LoggerAdapter(logger, extra)


# Default logging configuration dictionary
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
        'ai_practice_platform': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'werkzeug': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False
        },
        'sqlalchemy': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False
        }
    }
}
