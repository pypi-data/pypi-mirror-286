"""Copyright Senne vanden Berghe, 2024"""

from __future__ import annotations
from typing import Optional

import warnings
import __main__


class _Element:
    """This class is the base class!
    It allows to give a name equal to variable name (if well-defined).
    """

    def __init__(self) -> None:
        self._name: Optional[str] = None
        self._name_manually_set: bool = False

    def _update_name(self):
        """This functions checks the globals in main scope when called
        after instance is created and changes the instance name member to the (main) variable name.
        """
        counter = 0
        # I know this is a crime, leave me alone FBI.
        for key, value in __main__.__dict__.items():
            if not isinstance(value, _Element):
                continue
            if id(value) == id(self):
                self._name = key
                counter += 1
        if counter > 1:
            warnings.warn(f"""Multiple references found for {str(self)}! Current name: {
                          self._name}. Please avoid multiple references.""")
        elif counter == 0:  # Normally this cannot occur.
            warnings.warn(f"No references found for {str(self)}! Please give this instance a name via the name method.")

    @property
    def name(self):
        """name property

        Returns:
            Optional[str]: name of the element
        """
        if not self._name_manually_set:  # name must only be updated when name is NOT manually set
            self._update_name()
        return self._name

    @name.setter
    def name(self, name_val):
        if not isinstance(name_val, str):
            raise TypeError("Name must be a string!")
        self._name = name_val
        self._name_manually_set = True
