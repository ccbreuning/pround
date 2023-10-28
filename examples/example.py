# Nur um Pfade richtig verwenden zu können, kann man auch einfach mit Strings machen
from pathlib import Path

import numpy as np

from pround.pround import Pround

# Ein Paar Pseudo Daten
x = np.array([1.23456789, 2.3456789, 3.456789])
dx = np.array([0.123456789, 0.23456789, 0.3656789])
y = np.array([10.23456789, 20.3456789, 30.456789])
dy = np.array([1.23456789, 2.3456789, 3.456789])
z = np.array([42, 21, 100])

# Initialisiere das Objekt um die Tabelle zu erstellen
p = Pround(format="latex") # als format geht auch excel, wenn es in eine excel Tabelle geschrieben werden soll

# Alle daten werden als neue Spalte hinzugefügt. Der String am Anfang steht nachher als Überschrift der Spalte in der Tabelle.
# Gerundet wird an der ersten signifikanten Stelle des Fehlers (sollte das eine 1 oder eine 2 sein, dann wird eine stelle weiter gerundet). Da das uncertainties package verwendet wird, wird auch beim Fehler normal (und nicht immer auf) gerundet
p.add_column("x / cm", x, dx)
p.add_column("y / cm", y, dy)

# Man kann auch Werte ohne Fehler angeben. ndigits gibt dann an wo gerundet werden soll
p.add_column("z / cm", z, ndigits=1)

# Pfad zum Verzeichnis dieses Python skripts
cwd = Path(__file__).parent

# Speicer das ganze als tex datei ab. landscape gibt an ob das Dokument im Querformat sein soll
# Man kann filename auch weglassen, dann wird die Tabelle (ohne Präambel und so) im Terminal gedruckt
p.print_table(filename=cwd / "test.tex", landscape=True)