"""Cache class inherit from flask_caching.Cache
adjust its memoize method ot fit dynamic timeout
setting depending on the decorated function's result
"""
import base64
import functools
import hashlib
import inspect
import logging
from flask_caching import Cache, function_namespace


logger = logging.getLogger('flask_cache')


# pylint: disable=missing-docstring,broad-except,invalid-name
class SimpleCache(Cache):

    def memoize_simple(self, timeout=None, unless=None, forced_update=None, make_key=None):
        """
        Args:
            timeout (int|callable): int or callable
                 If callable, will take decorated function's result as first positional arg,
                 followed with other *args, **kwargs from decorated function. And it should
                 always return an integer even if nothing returns from decorated function.
            unless (callable):
                 It will take *args **kwargs from decorated function
                 and should return True/False to skip memoizing or not.
            forced_update (boolean|callable):
                 If callable, will take *args **kwargs from decorated function
                 and should return True/False to force update cache or not.
            make_key (callable):
                 It will take *args **kwargs from decorated function
                 And generate a custom cache key.
        """

        def memoize_simple(f):
            @functools.wraps(f)
            def decorated_function(*args, **kwargs):

                #: bypass cache
                if self._bypass_cache_simple(unless, *args, **kwargs):
                    logger.debug("Cache skipping bypass.")
                    return f(*args, **kwargs)

                try:
                    cache_key = decorated_function.make_cache_key(
                        f, *args, **kwargs
                    )

                    if callable(forced_update) and forced_update(*args, **kwargs) is True:
                        logger.debug("Cache skipping by forced updating.")
                        rv = None
                    else:
                        rv = self.cache.get(cache_key)
                        logger.debug("Get cache item for key: %s: %s", cache_key, rv)
                except Exception:
                    if self.app.debug:
                        raise
                    logger.exception("Exception possibly due to "
                                     "cache backend.")
                    return f(*args, **kwargs)

                if rv is None:
                    rv = f(*args, **kwargs)
                    try:
                        _timeout = decorated_function.cache_timeout
                        if callable(_timeout):
                            _timeout = _timeout(rv, *args, **kwargs)
                        self.cache.set(
                            cache_key, rv,
                            timeout=_timeout
                        )
                        logger.debug("Set cache item: %s: %s", cache_key, rv)
                    except Exception:
                        if self.app.debug:
                            raise
                        logger.exception("Exception possibly due to "
                                         "cache backend.")
                return rv

            decorated_function.uncached = f
            decorated_function.cache_timeout = timeout
            decorated_function.make_cache_key = make_key if callable(
                make_key) else self._memoize_make_cache_key_simple()
            decorated_function.delete_memoized = \
                lambda: self.delete_memoized(f)

            return decorated_function

        return memoize_simple

    def _memoize_make_cache_key_simple(self):
        """Function used to create the simple cache_key for memoized functions."""

        def make_cache_key(f, *args, **kwargs):

            fname, _ = function_namespace(f, args=args)
            if callable(f):
                keyargs, keykwargs = self._memoize_kwargs_to_args(
                    f, *args, **kwargs
                )
            else:
                keyargs, keykwargs = args, kwargs

            updated = u"{0}{1}{2}".format(fname, keyargs, keykwargs)
            cache_key = hashlib.md5()
            cache_key.update(updated.encode('utf-8'))
            cache_key = base64.b64encode(cache_key.digest())[:16]
            cache_key = cache_key.decode('utf-8')
            return cache_key

        return make_cache_key

    @staticmethod
    def _bypass_cache_simple(unless, *args, **kwargs):
        """Determines whether or not to bypass the cache by calling unless().
        Supports both unless() that takes in arguments and unless()
        that doesn't.
        """
        bypass_cache = False

        if callable(unless):
            argspec = inspect.getfullargspec(unless)

            # If unless() takes args, pass them in.
            if any((argspec.varargs, argspec.varkw, argspec.kwonlyargs, argspec.args,)):
                if argspec.kwonlydefaults:
                    kwargs.update(argspec.kwonlydefaults)
                bypass_cache = unless(*args, **kwargs)
            elif unless() is True:
                bypass_cache = True
        else:
            bypass_cache = bool(unless)

        return bypass_cache
