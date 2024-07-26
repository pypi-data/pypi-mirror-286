from importlib.metadata import version

from .model import Mater

Mater.__version__ = version("mater")  # to have the __version__ of the mater package
