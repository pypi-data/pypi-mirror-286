"""_summary_

Returns:
    _type_: _description_
"""

import random

from hello_baby.quotes import quotes


def get_quote() -> dict:
    """
    Get random quote

    Get randomly selected quote from database our programming quotes

    :return: selected quote
    :rtype: dict
    """

    return quotes[random.randint(0, len(quotes) - 1)]
