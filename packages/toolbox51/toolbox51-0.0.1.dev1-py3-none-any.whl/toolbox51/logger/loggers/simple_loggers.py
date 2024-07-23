import logging
from pathlib import Path

from ..handlers import get_console_handler, get_logfile_handler

def check_logger(name:str) -> bool:
    logger_dict = logging.Logger.manager.loggerDict
    return name in logger_dict
    
def new_logger(
    name:str, 
    level:int = logging.INFO,
    use_relative_path:bool = False,
    use_logfile:bool = False,
) -> logging.Logger:
    
    fmt = """ \
%(asctime)s%(_msecs)s | %(levelname)s | %(locate)s | %(funcName)s - %(message)s \
"""
    datefmt = "%Y-%m-%d %H:%M:%S"
    

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if(use_logfile):
        logger.addHandler(get_logfile_handler(
            level = level,
            fmt = fmt,
            datefmt = datefmt,
            use_relative_path = use_relative_path,
        ))
    logger.addHandler(get_console_handler(
        level = level,
        fmt = fmt,
        datefmt = datefmt,
        use_relative_path = use_relative_path,
    ))
    return logger

def get_logger(name:str):
    if(check_logger(name)):
        return logging.getLogger(name)
    else:
        return new_logger(name)

logger = new_logger(__name__, logging.DEBUG)
logger_relative = new_logger(__name__ + "_relative", logging.DEBUG, use_relative_path=True)

if __name__ == '__main__':

    logger.debug("DEBUG")
    logger.info("INFO")
    logger.warning("WARN")
    logger.error("ERROR")
    logger.critical("CRITICAL")