import functools

from types import FunctionType

from loguru import logger


def log_func(func):
    @functools.wraps(func)
    def logger_wrapper(*args, **kwargs):
        try:
            if getattr(func, 'is_class_method', False):
                logger.info(f'{func.__qualname__} Start call with args={args[1:]}, kwargs={kwargs}')
            else:
                logger.info(f'{func.__qualname__} Start call with args={args}, kwargs={kwargs}')
        except:  # noqa: E722
            pass
        try:
            result = func(*args, **kwargs)
        except ValueError as v_err:
            logger.warning(f'{func.__qualname__}: End call with value error {v_err}')
            raise v_err
        except Exception as err:
            logger.exception(f'{func.__qualname__} End call with exception: {err}', exc_info=err)
            raise err
        try:
            logger.info(f'{func.__qualname__} End call success')
        except:  # noqa: E722
            pass
        return result

    return logger_wrapper


def cls_method_log_func(func):
    func.is_class_method = True
    return log_func(func)


def disable_decorate_logger(f):
    f.disable_logger = True
    return f


def cls_apply_logger(cls):
    def isclassmethod(name):
        descriptor = vars(cls).get(name)
        if descriptor is not None:
            return isinstance(descriptor, classmethod)
        return False

    def isstaticmethod(name):
        descriptor = vars(cls).get(name)
        if descriptor is not None:
            return isinstance(descriptor, staticmethod)
        return False

    for attr, value in cls.__dict__.items():
        if (isinstance(value, FunctionType) or callable(value)) and not getattr(value, 'disable_logger', False):
            if isstaticmethod(attr):
                setattr(cls, attr, staticmethod(log_func(value.__func__)))
            else:
                setattr(cls, attr, log_func(value))
        elif isclassmethod(attr):
            value.__func__.is_class_method = True
            if not getattr(value.__func__, 'disable_logger', False):
                setattr(cls, attr, classmethod(log_func(value.__func__)))
    return cls
