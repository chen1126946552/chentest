# pylint: disable=missing-docstring
from pydatadeck.datasource.translation import get_translator

class BusinessError(Exception):
    """Generic error class."""
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


class OauthServiceError(BusinessError):
    """Oauth Service Error, generally caused by requiring auth_redirect_uri or
    exchanging auth code for token failed"""


class RequestHeaderError(BusinessError):
    """Raised when invalid or lost parameter(s) in request headers.

    This error generally corresponds to frontend requests without required
    header parameters like UID, SpaceId...
    """


class ArgumentError(BusinessError):
    """Raised when an invalid argument is supplied to some functions"""


class EntityNotFoundError(BusinessError):
    """Error representing a resource specified cannot be found"""


class EntityCreatingOrUpdatingError(BusinessError):
    """Error representing a resource specified cannot be found"""


class V2AdaptationError(BusinessError):
    """Adapt to v2 failed"""


class DsCodeUndefinedError(BusinessError):
    """Ds code undefined"""



class ErrorCode():
    """
    Business Error Codes
    """
    CONNECTION_NOT_FOUND = 'CONNECTION_NOT_FOUND'
