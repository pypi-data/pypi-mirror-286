"""
Random Quote Generator
======================

Get random quote from our database of programming wisdom
"""

try:
    from importlib.metadata import version as get_version

    __version__ = get_version("hello-baby")
except ImportError:
    __version__ = ""


# 导入 get_quote 函数
from .get_quote import get_quote

__all__ = ["__version__", "get_quote"]
