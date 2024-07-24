import functools
import warnings


def deprecated(version, reason):
    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            if func.__name__ == '__init__':
                cls_name = args[0].__class__.__name__
                warnings.warn(f"Class {cls_name} is deprecated and will be removed in version {version}. {reason}",
                              category=DeprecationWarning, stacklevel=2)
            else:
                warnings.warn(f"Function {func.__name__} is deprecated and will be removed in version {version}. {reason}",
                              category=DeprecationWarning, stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)
        return new_func
    return decorator
