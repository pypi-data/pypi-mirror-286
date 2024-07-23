from .models import *
from .predict import *
from .preprocess import *

from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "0.1.0"  # default
