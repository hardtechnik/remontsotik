try:
    from .config.local import *  # noqa
except ImportError:
    from .config.base import *  # noqa
