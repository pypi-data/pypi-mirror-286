"""Logger Module"""
import logging
from logging.config import dictConfig

log_level = logging.WARNING

logging_config = dict(
    version=1,
    formatters={
        'f':
        {
            'format': '%(asctime)s [Geometry3D %(levelname)s] %(message)s'
        },
    },
    handlers={
        'h':
        {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': log_level
        }
    },
    loggers=dict(
        geometry3d={
            'handlers': ['h'],
            'level': log_level
        },
    )
)

dictConfig(logging_config)
main_logger = logging.getLogger('geometry3d')


def get_main_logger():
    '''
    **Input:**

    No Input

    **Output:**

    main_logger: The logger instance
    '''
    # global main_logger
    return main_logger
