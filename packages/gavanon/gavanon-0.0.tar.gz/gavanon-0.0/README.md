# gavanon
Python package for the Ghent University Gavanon course (Geavanceerd Analoog Ontwerp, English: Advanced Analog Design ).

This package let you define transistors and voltage/current sources so you can basically make an operational amplifier.
The data of the transistors and sources is translated to a skill file which can be inported in Cadence.

Small example:
```python
from gavanon import (Transistor, DoubleTransistor, NMOS, PMOS,
                     VoltageSource, CurrentSource,
                     CadenceCell, CadenceLib)

Mdiff = DoubleTransistor("nmos")
Mdiff.ID = 5e-3  # Choose current
Mdiff.gmoverid = 10 # Choose gm over ID
Mdiff.gm = Mdiff.gmoverid*Mdiff.ID
W_over_L = Mdiff.gm**2/2/Mdiff.ID/NMOS.KP_n  # Piecewise linear model
Mdiff.W = W_over_L*Mdiff.L
Mdiff.ng = 10  # Set number of gates

ota_cell = CadenceCell("Simple_OTA")
ota_cell += Mdiff 

lib = CadenceLib("CadenceLib")
lib += ota_cell
lib.export_sizing("simple_ota_sizing.il")
```

For more information see the simple_ota jupyter notebook in tests.