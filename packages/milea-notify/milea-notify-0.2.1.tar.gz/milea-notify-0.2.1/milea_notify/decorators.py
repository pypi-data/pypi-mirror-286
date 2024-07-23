import logging

registered_milea_notify_functions = set()
registered_functions = set()

def milea_notify(label=None):
    def decorator(func):

        func_name = func.__name__
        module_name = func.__module__.split('.')[0]

        # Überprüfen, ob func_name bereits in registered_milea_notify_functions vorhanden ist
        if func_name in registered_functions:
            logging.warning("Function %s is already registered. Skipping." % func_name)
        else:
            registered_functions.add(func_name)
            registered_milea_notify_functions.add((module_name, func_name, label))
            logging.info('Update registered milea notify functions: %s' % list(registered_milea_notify_functions))

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
    return decorator
