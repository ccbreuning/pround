from pathlib import Path

import numpy as np

from src.pround.pround import Pround

if __name__ == "__main__":
    x = np.array([1.23456789, 2.3456789, 3.456789])
    dx = np.array([0.123456789, 0.23456789, 0.3656789])
    y = np.array([10.23456789, 20.3456789, 30.456789])
    dy = np.array([1.23456789, 2.3456789, 3.456789])
    z = np.array([42, 21, 100])
    
    p = Pround(format="latex")
    p.add_column("x / cm", x, dx)
    p.add_column("y / cm", y, dy)
    p.add_column("z / cm", z, ndigits = 1)
    cwd = Path(__file__).parent
    p.print_table(filename=cwd / "test.tex")