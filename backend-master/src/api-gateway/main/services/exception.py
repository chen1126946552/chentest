# pylint: disable=missing-docstring
from services.translate import get_translator

class ServiceError(Exception):
    """Generic error"""

    def __init__(self, message="", error_code=None, locale="en_US"):
        """
        Constructs a new instance
        Args:
            message (str, optional): Defaults to None. Error message.
            error_code (str, optional): Defaults to None. Error code.
            If it's a predefined code, it will prefix the localized error message
            locale (str, optional): en_US, ja_JP, zh_CN
        """

        super().__init__(message)
        # Both field will be used in __str__, make sure it is defined
        self.message = message
        self.error_code = error_code

        if error_code:
            self.error_code = error_code
            if hasattr(ErrorCode, error_code):
                _ = get_translator(locale, "error")
                error_message = _(getattr(ErrorCode, error_code))
                self.message = '{} {}'.format(error_message, message)

    def __str__(self):
        return f'{self.error_code}: {self.message}'


class V2AdaptorError(ServiceError):
    """v2 adapting error"""



class ErrorCode():
    """
    Gateway Error Codes
    """
    SEGMENT_NOT_EXIST = 'SEGMENT_NOT_EXIST'
