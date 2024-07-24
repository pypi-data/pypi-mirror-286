from timpypi.timpypi.utils import __log__


def exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            __log__(f"An error occurred in {func.__name__}: {e}")
            return None
    return wrapper
