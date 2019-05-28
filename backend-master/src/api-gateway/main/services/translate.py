"""Functions for text translation"""

import os
from pydatadeck.datasource.translation import get_translator as _get_translator


def get_translator(locale, domain):
    """
    Gets translator for translating fields.
    """

    locale_dir = os.path.join(os.path.dirname(__file__), '../locales')
    return _get_translator(locale, domain, locale_dir=locale_dir)
