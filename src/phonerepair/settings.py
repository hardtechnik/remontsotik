try:
    from .config.local import *
except ImportError:
    from .config.base import *
