import functools

from .exceptions import InitializationError


def check_initialization(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self._initialized:
            raise InitializationError('Please call "detect_scanners" '
                                      'method first.')
        return method(self, *args, **kwargs)
    return wrapper
