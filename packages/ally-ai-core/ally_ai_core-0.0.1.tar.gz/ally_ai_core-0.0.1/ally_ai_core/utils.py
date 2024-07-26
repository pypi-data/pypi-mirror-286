from contextlib import contextmanager
import logging
import os

def get_loglevel() -> int:
    """
    returns log level 
        if LOG_LEVEL is in environment variables
    or
        'INFO'
    """
    _default_level = 'INFO'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', _default_level).upper()
    if LOG_LEVEL == '':
        LOG_LEVEL = _default_level

    return logging._nameToLevel[LOG_LEVEL]

LOG_LEVEL = get_loglevel()

@contextmanager
def log_step(name: str, level=LOG_LEVEL, raise_exception: bool = True):
    try:
        logging.log(level=level, msg=f"Step({name}): Executing...")
        yield
        logging.log(level=level, msg=f"Step({name}): Executed.")
    except Exception as ex:
        logging.error(f"Step({name}): Failed! Reason: {ex}")

        if raise_exception:
            raise

def get_value_or_default(key:str, default:any, **kwargs):
    """
    returns kwargs value or default
        if key is in kwargs
    or
        default value
    """
    return kwargs[key] if key in kwargs else default