"""
This file is used to define basic calculate functions used for
calculated field service, AND, provide a basic exec namespace template
BE CAREFUL IF TO CHANGE THIS FILE
"""


def _sum(*args, **kwargs):
    """base calculated function"""
    raise NotImplementedError('sum is not implemented yet')


def _avg(*args, **kwargs):
    """base calculated function"""
    raise NotImplementedError('sum is not implemented yet')


def _max(*args, **kwargs):
    """base calculated function"""
    raise NotImplementedError('sum is not implemented yet')


def _min(*args, **kwargs):
    """base calculated function"""
    raise NotImplementedError('sum is not implemented yet')


def _count(*args, **kwargs):
    """base calculated function"""
    raise NotImplementedError('sum is not implemented yet')


def _distinct_count(*args, **kwargs):
    """base calculated function"""
    raise NotImplementedError('sum is not implemented yet')


calf_buildin_function_map = {
    'Sum': _sum,
    'Avg': _avg,
    'Max': _max,
    'Min': _min,
    'Count': _count,
    'Distinct_count': _distinct_count
}

GLOBAL_NAME_SPACE = globals()

GLOBAL_NAME_SPACE.update(
    calf_buildin_function_map
)
