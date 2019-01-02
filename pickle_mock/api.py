import os
import types
import pickle
import inspect
import re


def __getstate__(self):
    state = {}
    for attr in self.__dict__:
        if attr in ('__getstate__', '__setstate__'):
            continue
        try:
            pickle.dumps(self.__dict__[attr])
            state.update({attr: self.__dict__[attr]})
        except TypeError as e:
            state.update({attr: e})

    return state


def __setstate__(self, state):
    for attr, value in state.items():
        setattr(self, attr, value)


class AutoMock(object):
    directory = ''

    def __init__(self, method, method_args=(), method_kwargs=None):
        self.method = method
        self.method_args = method_args
        self.method_kwargs = method_kwargs

    def mock_method(self, *args, **kwargs):

        if set(args) == set(self.method_args) and kwargs == self.method_kwargs:
            pickled_results = self.get_method_response()
            if pickled_results:
                return pickled_results

        f_locals = inspect.currentframe().f_back.f_locals
        for _ in kwargs:
            f_locals.pop(_)

        obj = None
        for loc in f_locals:
            if f_locals[loc] not in args:
                obj = f_locals[loc]

        r = self.method(obj, *args, **kwargs)
        self.save_method_response(data=r)

        return r

    @classmethod
    def auto_mock(cls, method, method_args=(), method_kwargs=None):
        """ Automatically mock an arbitrary class method.

        Instead of the actual method being called, a mox method will be called instead
        as long as the method_args and method_kwargs match the atcual method being called.

        :param method:  the method which you would like to mock
        :param method_args: the arguments to the method you would like to mock
        :param method_kwargs: the keyword arguments to the method you would like to mock
        :return: the mock method
        """
        pm = AutoMock(method, method_args, method_kwargs)
        return pm.mock_method

    def get_method_response(self):
        try:
            with open(os.path.join(self.directory, self.auto_filename()), 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            pass

    def save_method_response(self, data):
        data.__getstate__ = types.MethodType(__getstate__, data)
        data.__setstate__ = types.MethodType(__setstate__, data)

        with open(os.path.join(self.directory, self.auto_filename()), 'wb') as f:
            pickle.dump(data, f)

    def auto_filename(self):
        """ Provide an identifying filename to the method being mocked.

        Note this is a horrible solution right now.

        The method is uniquely identified by its name, its args, and its kwargs:
        """
        method_str = 'method-' + re.search('^<[A-z]*\s(.*)\sat', str(self.method)).group(1).replace('.',
                                                                                                    '-').lower() + '--'
        args_str = 'args-' + '-'.join(self.method_args).replace(':', '').replace('/', '').replace('.', '') + '--'
        kwargs_str = 'kwargs-' + '-'.join(
            ['{}={}'.format(_, self.method_kwargs[_]) for _ in sorted(self.method_kwargs)])
        return method_str + args_str + kwargs_str
