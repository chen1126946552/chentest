'''
Flask thread executor
'''
from concurrent.futures import ThreadPoolExecutor
from flask import copy_current_request_context, g, request, current_app
from werkzeug.local import LocalProxy
from werkzeug.datastructures import Headers

def _get_request():
    """
    Return DummyRequest if in worker thread, otherwise return real flask request
    """
    if 'is_worker' in g:
        return g.dummy_request
    else:
        return request

request_proxy = LocalProxy(_get_request)

def propagate_exceptions_callback(future):
    exc = future.exception()
    if exc:
        raise exc

class DummyRequest:
    pass

class Executor:
    """
    Flask thread executor taking care of AppContext and RequestContext
    """

    DEFAUL_MAX_WORKERS = 5
    REQUEST_ATTRS = [
        'args',
        'full_path',
        'headers',
        'json',
        'method',
        'url'
    ]

    def __init__(self, app=None):
        self.app = app
        self._executor = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize application.
        """
        executor_max_workers = app.config.setdefault('EXECUTOR_MAX_WORKERS',
                                                     Executor.DEFAUL_MAX_WORKERS)
        self._executor = ThreadPoolExecutor(executor_max_workers)

    def _get_dummy_request(self, flask_request):
        result = DummyRequest()
        for k in Executor.REQUEST_ATTRS:
            val = getattr(flask_request, k)
            if isinstance(val, (dict, Headers)):
                setattr(result, k, dict(val.items()))
            else:
                setattr(result, k, val)
        return result

    def _copy_current_app_context(self, func):
        app_context = current_app.app_context()
        dummy_request = self._get_dummy_request(request)

        def wrapper(*args, **kwargs):
            with app_context:
                g.is_worker = True
                g.dummy_request = dummy_request
                return func(*args, **kwargs)

        return wrapper


    def _prepare_func(self, func):
        func = copy_current_request_context(func)
        func = self._copy_current_app_context(func)
        return func

    def submit(self, func, *args, **kwargs):
        """Schedules the callable, func, to be executed
        """
        func = self._prepare_func(func)
        future = self._executor.submit(func, *args, **kwargs)
        future.add_done_callback(propagate_exceptions_callback)
        return future
