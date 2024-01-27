def classdecorator(decorator):
    def wrapper(self=None, *a, **kw):
        return lambda func: decorator(func, *a, **kw)
    return wrapper








