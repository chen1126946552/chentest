"""common utils in gateway"""
from collections import UserDict
from .exception import V2AdaptorError


# pylint: disable=too-many-ancestors,useless-super-delegation
class NotMatchRaiseExceptionDict(UserDict):
    """a custom dict, when a key is not found will raise an exception"""
    def __init__(self, *args, **kwargs):
        super(NotMatchRaiseExceptionDict, self).__init__(*args, **kwargs)

    def __missing__(self, key):
        # special case, if key is an empty string, return none instead of raise an exception
        if not key:
            return None
        raise V2AdaptorError("Can not match key: %s" % key)
