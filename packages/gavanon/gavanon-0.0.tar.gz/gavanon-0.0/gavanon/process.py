""" Copyright Senne Vanden Berghe, 2024
This data is adapted from prof. dr. ir. Pieter Rombouts Matlab script from the Gavanon course.

This file contains the two dataclasses containing al the parameters for the 0.35µm technology used in
the Advanced Analog Design course. The dataclasses are regarding the NMOS and PMOS transistors
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class NMOS:
    """Contains all needed values of the NMOS transistor in the 0.35µm technology.
    Values:
        * KP_n = 170e-6 A/V²
        * n = 1.3
        * VT = 0.7 V
        * VEarly = 18e6 V/m
        * vsat = 8e4 m/s
        * Cox = 6e-3 F/m²
        * Kf = 1.6e-26 C²/m²
        * CDB0 = 0.5e-9 F/m
        * CSB0 = 0.5e-9 F/m
        * CGS0 = 0.1e-9 F/m
        * CGD0 = 0.1e-9 F/m
    """
    KP_n = 170e-6
    n = 1.3
    VT = 0.7
    VEarly = 18e6
    vsat = 8e4
    Cox = 6e-3
    Kf = 1.6e-26
    CDB0 = 0.5e-9
    CSB0 = 0.5e-9
    CGS0 = 0.1e-9
    CGD0 = 0.1e-9


@dataclass(frozen=True)
class PMOS:
    """Contains all needed values of the PMOS transistor in the 0.35µm technology
    Values:
        * KP_n = 50e-6 A/V²
        * n = 1.3
        * VT = 0.7 V
        * VEarly = 8e6 V/m
        * vsat = 8e4 m/s
        * Cox = 6e-3 F/m²
        * Kf = 4e-28 C²/m²
        * CDB0 = 0.5e-9 F/m
        * CSB0 = 0.5e-9 F/m
        * CGD0 = 0.09e-9 F/m
        * CGS0 = 0.1e-9 F/m
    """
    KP_n = 50e-6
    n = 1.3
    VT = 0.7
    VEarly = 8e6
    vsat = 8e4
    Cox = 6e-3
    Kf = 4e-28
    CDB0 = 0.5e-9
    CSB0 = 0.5e-9
    CGD0 = 0.09e-9
    CGS0 = 0.1e-9
