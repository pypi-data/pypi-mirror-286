r"""
无第三方依赖的logger，在vscode下可以显示完整路径与行号，支持vscode的一键跳转
"""

from .loggers import logger as logger
from .loggers import logger_relative as logger_relative