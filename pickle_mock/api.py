from typing import Callable
import functools
import pickle


def pickle_mock(func: Callable, *args, **kwargs):
    """ pickle mock is a decorator with arguments
    :param func: this is the function you want to mock (but only if a pickle is available)
    :param args: these are the positional arguments to func
    :param kwargs: these are the keyword arguments to func
    """

    def get_func():
        return func

    @functools.wraps(func)
    def decorator(decorated_func: Callable):
        """ decorator is the actual decorator.
        :param decorated_func: this is the function being decorated, typically a test function with no arguments
        """
        print('hi, i am decorator! I return wrapper')

        @functools.wraps(decorated_func)
        def wrapper():
            """ wrapper is the function replacing the decorator """
            file = '{}.pickle'.format(decorated_func.__name__)  # the name of the file is the name of the test

            try:
                with open(file, 'rb') as f:
                    pickled_response = pickle.load(f)
                    return pickled_response

            except FileNotFoundError:
                pass

            # in this case we can replace func with a decorator that pickles after it is called
            func = pickle_the_func(get_func(), file=file)  # this doesn't work...what's the point of the args and kwargs?

            # now call the decorated_func (the test function)
            return decorated_func()

        return wrapper

    return decorator


def pickle_the_func(func, file):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        r = func(*args, **kwargs)
        with open(file, 'wb') as f:
            pickle.dump(r, f)
        return r

    return wrapper
