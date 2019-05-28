'''Service exception classes'''

class ServiceError(Exception):
    '''Generic service error.'''


class EntityNotFoundError(Exception):
    '''Error representing a resource specified cannot be found'''


class ObjectTypeError(Exception):
    '''Object type is error'''
