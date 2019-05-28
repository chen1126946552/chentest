"""common properties"""
from collections import defaultdict


class Fields:
    """fields related properties"""
    type_order = defaultdict(
        lambda: -1, {'number': 0, 'string': 1, 'date': 2}
    )
    number_format_order = defaultdict(
        lambda: -1, {'number': 0, 'currency': 1, 'percentage': 2, 'durationInSeconds': 3}
    )
    granularity_format_order = defaultdict(
        lambda: -1, {'year': 0, 'quarter': 1, 'month': 2, 'week': 3,
                     'day': 4, 'hour': 5, 'minute': 6, 'second': 7, 'millisecond': 8}
    )
