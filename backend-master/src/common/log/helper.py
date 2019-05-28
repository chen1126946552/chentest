"""
Logging related helpers.
"""


import traceback

def log_exception(logger, ex):
    """
    Logs an exception with Error level with its type,
    message and stack trace.

    Args:
        logger (Logger): The logger.
        ex (Exception): The exception
    """

    stack = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
    logger.error('%s: %s\n%s', type(ex), str(ex), ''.join(stack))
