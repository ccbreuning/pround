from pathlib import Path

import numpy as np
import uncertainties.unumpy as unp

from pround.pround import Pround

# Random data
x = np.array([1.23456789, 2.3456789, 3.456789])
dx = np.array([0.123456789, 0.23456789, 0.3656789])
y = np.array([10.23456789, 20.3456789, 30.456789])
dy = np.array([1.23456789, 2.3456789, 3.456789])
z = np.array([42, 21, 100])

# Create the object das Objekt um die Tabelle zu erstellen
# If you later want an excel table use "excel" instead of "latex"
p = Pround(format="latex") 

# All data are added in columns. The first argument will be the columns name in the table.
# THus, all arrays must have the same length
# The rounding is specified in the README
p.add_column("x / cm", x, uncertainties=dx)


# You can also provide values without uncertainties and the values are rounded to the specified number of digits (default is 2) after the decimal point
p.add_column("z / cm", z, ndigits=1)

# You can also add uarrays from uncertainties
y_unc = unp.uarray(y, dy)
p.add_column("y / cm", y_unc)

# Path to this file
cwd = Path(__file__).parent

# Save table in latex file (can be complied with e.g. lualatex). Landscape is optional and defines the orientation of the latex file
# If filename is not provided the table is printed to stdout
p.print_table(filename=cwd / "test.tex", landscape=True)