from collections import OrderedDict
from typing import Any


class LimitedDict(OrderedDict):
    """
    A dictionary with a limit on the number of items it can store.

    When the limit is reached, the oldest item is removed.

    Parameters
    ----------
    limit : int
        The maximum number of items to store.
    """

    def __init__(self, limit: int, *args, **kwargs) -> None:
        self.limit = limit
        super().__init__(*args, **kwargs)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Sets the value of the key.
        """
        if key in self:
            del self[key]
        elif len(self) >= self.limit:
            self.popitem(last=False)
        super().__setitem__(key, value)

    def __contains__(self, key: str) -> bool:
        """
        Returns whether the key is in the dictionary.
        """
        return key in self.keys()
