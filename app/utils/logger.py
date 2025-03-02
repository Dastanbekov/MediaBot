import logging
import logging.handlers
import os
from datetime import datetime

def setup_logger():
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # Create handlers
    # File handler for all logs
    all_logs_file = os.path.join(logs_dir, f'bot_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.handlers.RotatingFileHandler(
        all_logs_file,
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)

    # File handler for errors
    error_logs_file = os.path.join(logs_dir, f'errors_{datetime.now().strftime("%Y%m%d")}.log')
    error_file_handler = logging.handlers.RotatingFileHandler(
        error_logs_file,
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_file_handler.setFormatter(file_formatter)
    error_file_handler.setLevel(logging.ERROR)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove any existing handlers
    logger.handlers = []

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)
    logger.addHandler(console_handler)

    # Create specific loggers
    loggers = {
        'bot': logging.getLogger('bot'),
        'database': logging.getLogger('database'),
        'youtube': logging.getLogger('youtube'),
        'admin': logging.getLogger('admin'),
        'user': logging.getLogger('user')
    }

    for logger_name, logger_instance in loggers.items():
        logger_instance.setLevel(logging.INFO)

    return loggers

# Create and export logger instances
loggers = setup_logger()
bot_logger = loggers['bot']
db_logger = loggers['database']
yt_logger = loggers['youtube']
admin_logger = loggers['admin']
user_logger = loggers['user'] 