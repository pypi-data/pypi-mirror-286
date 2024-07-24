# Copyright Senne Vanden Berghe, 2024

from __future__ import annotations
from typing import Optional, Union, Literal
import warnings

from ._element import _Element


Catergory = Literal["nmos", "pmos"]


class Transistor(_Element):
    """Transistor class contains all the parameters of the transistor.
    """

    def __init__(self, catergory: Optional[Catergory] = None) -> None:
        self.__L: float = 0.35e-6
        self.__W: float = 0
        self.__gm: float = 0
        self.__gmoverid: float = 0
        self.__ID: float = 0
        self.__ng: int = 0
        self.__category: Optional[Catergory] = (
            catergory if catergory in ["nmos", "pmos"] else None
        )

        super().__init__()

    @property
    def L(self):
        return self.__L

    @L.setter
    def L(self, l_val):
        if not (isinstance(l_val, float) or isinstance(l_val, int)):
            raise TypeError("Length must be a float or int")
        if l_val <= 0:
            raise ValueError("Length must be higher than 0")
        self.__L = l_val

    @property
    def W(self):
        return self.__W

    @W.setter
    def W(self, w_val):
        if not (isinstance(w_val, float) or isinstance(w_val, int)):
            raise TypeError("Width must be a float or int")
        if w_val <= 0:
            raise ValueError("Width must be higher than 0")
        self.__W = w_val

    @property
    def gm(self):
        return self.__gm

    @gm.setter
    def gm(self, gm_val):
        if not (isinstance(gm_val, float) or isinstance(gm_val, int)):
            raise TypeError("gm must be a float or int")
        if gm_val <= 0:
            raise ValueError("gm must be higher than 0")
        self.__gm = gm_val

    @property
    def gmoverid(self):
        return self.__gmoverid

    @gmoverid.setter
    def gmoverid(self, gmoverid_val):
        if not (isinstance(gmoverid_val, float) or isinstance(gmoverid_val, int)):
            raise TypeError("gmoverid must be a float or int")
        if gmoverid_val <= 0:
            raise ValueError("gmoverid must be higher than 0")
        self.__gmoverid = gmoverid_val

    @property
    def ID(self):
        return self.__ID

    @ID.setter
    def ID(self, ID_val):
        if not (isinstance(ID_val, float) or isinstance(ID_val, int)):
            raise TypeError("ID must be a float or int")
        if ID_val <= 0:
            raise ValueError("ID must be higher than 0")
        self.__ID = ID_val

    @property
    def ng(self):
        return self.__ng

    @ng.setter
    def ng(self, ng_val):
        if not (isinstance(ng_val, float) or isinstance(ng_val, int)):
            raise TypeError("ng must be a float")
        if ng_val <= 0:
            raise ValueError("ng must be higher than 0")
        if isinstance(ng_val, float):
            self.__ng = round(ng_val)
            warnings.warn(f"Converted ng float to int. Result: {self.__ng}.")
        else:
            self.__ng = ng_val

    @property
    def catergory(self):
        return self.__category

    @catergory.setter
    def catergory(self, catergory_val):
        if not isinstance(catergory_val, str):
            raise TypeError('category must be "nmos" or "pmos"')

        if catergory_val == "nmos":
            self.__category = "nmos"
        elif catergory_val == "pmos":
            self.__category = "pmos"
        else:
            self.__category = None

    def _properties(self) -> list:
        return [
            self.name,
            f"wtot={self.__W*1e6:.3f}u",
            f"l={self.__L*1e6:.3f}u",
            f"ng={self.__ng}",
        ]

    def __str__(self):
        return " ".join(
            self._properties() + [f"ID={self.__ID*1e6:.3f}u", f"gmoverid={self.__gmoverid:.2f}"]
        )

    def __truediv__(self, other: Union[float, int]):
        """Performs an impedance scaling of factor `other` and returns a new transistor instance.

        Args:
            other (Union[float, int]): impedance scale factor

        Returns:
            Transistor: impedance scaled transistor
        """
        if not (isinstance(other, float) or isinstance(other, int)):
            warnings.warn(
                "Transistor can only be divided by int or float! Returning None"
            )
            return None
        new_transistor = Transistor()

        # impedance scalings factors
        new_transistor.ID = self.__ID / other
        new_transistor.ng = max(round(self.__ng / other), 1)
        new_transistor.W = self.__W / other

        # non scalable factors
        new_transistor.L = self.__L
        new_transistor.gmoverid = self.__gmoverid

        return new_transistor


class DoubleTransistor(Transistor):
    """Double transistor with the same sizing, for a differential pair for example.
    """

    def __init__(
        self,
        catergory: Optional[Catergory] = None,
        first_suffix: str = "_a",
        second_suffix: str = "_b",
    ) -> None:
        if not isinstance(first_suffix, str):
            warnings.warn("First suffix must be a string! Default value (_a) is used.")
            self._second_suffix: str = "_a"
        else:
            self._first_suffix: str = first_suffix

        if not isinstance(second_suffix, str):
            warnings.warn("Second suffix must be a string! Default value (_b) is used.")
            self._second_suffix: str = "_b"
        else:
            self._second_suffix: str = second_suffix
        super().__init__()

    def _properties(self) -> list:
        prop = super()._properties()
        prop[0] = prop[0] + self._first_suffix + "," + prop[0] + self._second_suffix
        return prop
