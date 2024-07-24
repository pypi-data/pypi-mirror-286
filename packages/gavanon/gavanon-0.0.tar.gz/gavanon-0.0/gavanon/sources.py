"""Copyright Senne vanden Berghe, 2024
This file contains all classes regarding to sources in the design.
"""

from __future__ import annotations
from typing import Optional, Union

from ._element import _Element


class Source(_Element):
    """Source base class"""


class VoltageSource(Source):
    """Voltage source

    Args:
        V (Optional[Union[float, int]], optional): Voltage in Volt. Defaults to None.
    """

    def __init__(self, V: Optional[Union[float, int]] = None) -> None:
        if V:
            self.V = V  # use setter for santization
        self._V: float = 0
        super().__init__()

    @property
    def V(self) -> float:
        """Voltage source voltage property

        Returns:
            float: Voltage source voltage in Volt
        """
        return self._V

    @V.setter
    def V(self, v_val):
        if not isinstance(v_val, (int, float)):
            raise TypeError("Voltage must be a float!")
        self._V = float(v_val)

    def _properties(self) -> list:
        """Function to generate skill script.\n
        This function does not give any relevant functionality for the end user.

        Returns:
            list: skill script paramters
        """
        return [self.name, f"vdc={self._V:.3f}"]


class CurrentSource(Source):
    """Current source

    Args:
        I (Optional[Union[float, int]], optional): Current in Ampère. Defaults to None.
    """

    def __init__(self, I: Optional[Union[float, int]] = None) -> None:
        if I:
            self.I = I  # use setter for santization
        self._I: float = 0
        super().__init__()

    @property
    def I(self) -> float:
        """Current source current property

        Returns:
            float: Current source current in Ampère
        """
        return self._I

    @I.setter
    def I(self, i_val):
        if not isinstance(i_val, (int, float)):
            raise TypeError("Current must be a float!")
        self._I = float(i_val)

    def _properties(self) -> list:
        """Function to generate skill script.\n
        This function does not give any relevant functionality for the end user.

        Returns:
            list: skill script paramters
        """
        return [self.name, f"idc={self._I*1e6:.3f}u"]
