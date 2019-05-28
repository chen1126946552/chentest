"""common properties"""
from collections import defaultdict


# pylint: disable=invalid-name
def cmp(x, y):
    """
    Replacement for built-in function cmp that was removed in Python 3

    Compare the two objects x and y and return an integer according to
    the outcome. The return value is negative if x < y, zero if x == y
    and strictly positive if x > y.
    """
    return (x > y) - (x < y)


class Fields:
    """fields related properties"""

    class Granularity:
        """date type field granularity"""
        YEAR = 'year'
        QUARTER = 'quarter'
        MONTH = 'month'
        WEEK = 'week'
        DAY = 'day'
        HOUR = 'hour'
        MINUTE = 'minute'
        SECOND = 'second'
        MILLISECOND = 'millisecond'

        granularity_order_map = defaultdict(
            lambda: float("inf"),
            {
                YEAR: 9, QUARTER: 8, MONTH: 7, WEEK: 6,
                DAY: 5, HOUR: 4, MINUTE: 3, SECOND: 2,
                MILLISECOND: 1
            }
        )

        def __init__(self, code=None):
            self.code = code
            self._set_seq()

        def _set_seq(self):
            if self.code not in self.granularity_order_map.keys():
                raise ValueError('')
            self.seq = self.granularity_order_map[self.code]

        def __cmp__(self, other):
            return cmp(self.seq, other.seq)

    class CompareWithPrevious:
        """compare with previous function code"""
        YEAR_OVER_YEAR = 'yoy'
        MONTH_OVER_MONTH = 'mom'
        PERIOD_OVER_PERIOD = 'pop'

    field_default_value = {
        'allowFilter': True,
        'allowSegment': False,
        'allowGroupby': False,
        'allowAggregation': False
    }


# pylint: disable=missing-docstring
class Constant:
    class Data:
        COMPUTING_PRECISION = 4

    class Cache:
        """Cache related constants"""
        class Timeout:
            """cache timeout in seconds"""

            # non-specific cache default timeout
            default = 50

            # data-fetching-data-cache-timeout-policy:
            realtime = 30
            normal = 600
            immutable = 3600

            # data-fetching-properties-cache-timeout-policy: segments|fields|path
            inert = 3600
