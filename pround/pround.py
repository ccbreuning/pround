import math
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import uncertainties as unc
import uncertainties.unumpy as unp


class Pround:
    
    def __init__(self, format: str = "latex") -> None:
        """Initiate a Pround object.
        Print measurements (with uncertainties) in a table in a nice, rounded way.
        
        Parameters
        ----------
        format : str
            The format of the table. Default is 'latex'. One of 'latex' or 'excel'.
        
        """
        self.data = pd.DataFrame()
        self.format = format


    def __round_numpy(self, values: np.ndarray, errors: np.ndarray = None, ndigits: int = 2) -> List[str]:
        """Round a numpy array of measurements with uncertainties.

        Parameters
        ----------
        values : np.ndarray
            values
        errors : np.ndarray
            errors
        ndigits : int, optional
            The number of digits to round to. Default is 2. This is only used if uncertainties is None.

        Returns
        -------
        List[str]
            rounded values as string
        """
        result = []
        if errors is None:
            result = [f"{x:.{ndigits}f}" for x in values]
        else:
            uncert_array = unp.uarray(values, errors)
            result = self.__round_unumpy(uncert_array)
        return result
    

    def __round_unumpy(self, values: unp.uarray) -> List[str]:
        """Stringify a unumpy array of measurements with uncertainties.

        Parameters
        ----------
        values : unp.uarray
            values with uncertainties

        Returns
        -------
        List[str]
            Rounded strings of uncertainties
        """
        result = []
        for val in values:
            precision = int(-np.floor(np.log10(val.s)))
            first_uncert_digit = np.floor(val.s * 10 ** precision)
            if int(np.abs(first_uncert_digit)) == 1 or int(np.abs(first_uncert_digit)) == 2:
                precision += 1 
            if precision < 0:
                v = round(val.n, precision)
                s = round(val.s, precision)
                print(val.s, precision)
            else:
                v = val.n
                s = val.s
            rounded_val = ('{0:.' + str(max(precision, 0)) + 'f}').format(v)
            rounded_err = ('{0:.' + str(max(precision, 0)) + 'f}').format(s)
            if self.format == "latex":
                result.append(f"\\num{{{rounded_val} +- {rounded_err}}}")
            else:
                result.append(f"{rounded_val} +- {rounded_err}")

        return result
        

    def add_column(self, header: str, values: np.ndarray, uncertainties: np.ndarray = None, ndigits: int = 2) -> None:
        """Add columns to the Pround object.
        
        Parameters
        ----------
        header : str
            The header of the column.
        values : np.array | unp.uarray
            The values of the column.
        uncertainties : np.array, optional
            The uncertainties of the column.
        ndigits : int, optional
            The number of digits to round to. Default is 2. This is only used if uncertainties is None.
        
        """
        if uncertainties is not None:
            if values.shape != uncertainties.shape:
                raise ValueError("Values and uncertainties must have the same shape.")
        if values.ndim != 1:
            raise ValueError("Values and uncertainties must be 1D arrays.")
        if len(values) > 0:
            if isinstance(values[0], unc.core.Variable):
                rounded_values = self.__round_unumpy(values)
            elif isinstance(values, np.ndarray):
                rounded_values = self.__round_numpy(values, uncertainties, ndigits)
            else:
                try:
                    values = values.to_numpy()
                    uncertainties = uncertainties.to_numpy()
                    rounded_values = self.__round_numpy(values, uncertainties, ndigits)
                except:
                    raise ValueError("Values and uncertainties must be numpy arrays or uncertainties uarrays.")
        self.data[header] = rounded_values

    def print_table(self, filename: str = None, landscape: bool = True, min: int = 0, max: int = None) -> None:
        """Print the data frame as a table.

        Parameters
        ----------
        filename : str | Path, optional
            filename if the table is to be saved to a file, by default None
        landscape : bool, optional
            Whether the table should be printed in landscape mode, by default True
        min : int, optional
            The first row to print, by default 0
        max : int, optional
            The last row to print, by default None. Python slcing is used, thus, begin counging at 0.
        """
        if self.format == "excel":
            if filename is None:
                print(self.data)
            else:
                self.data.to_excel(filename, index=False)
        elif self.format == "latex":
            latex_str = f"\\begin{{tabular}}{{{'c' * len(self.data.columns)}}}\\toprule\n"
            latex_str += f"{' & '.join(self.data.columns)}\\\\ \n\\midrule\n"
            rows = self.data.values
            rows = rows[min:max] if max is not None else rows[min:]
            for row in rows:
                latex_str += f"{' & '.join(row)}\\\\\n"
            latex_str += "\\bottomrule\n\\end{tabular}\n"
            if filename is None:
                print(latex_str)
            else:
                with open(filename, "w") as f:
                    landscape = ", paper=landscape" if landscape else ""
                    preamble = "\\documentclass{scrartcl}\n"
                    preamble += f"\\KOMAoptions{{fontsize=12pt, paper=a4{landscape}}}\n"
                    preamble += "\\KOMAoptions{DIV=20}\n"
                    preamble += "\\usepackage{booktabs}\n"
                    preamble += "\\usepackage{amsfonts}\n"
                    preamble += "\\usepackage{amsmath,amssymb}\n"
                    preamble += "\\usepackage{physics}\n"
                    preamble += "\\usepackage[separate-uncertainty=true]{siunitx}\n"
                    preamble += "\\usepackage[utf8]{inputenc}\n"
                    preamble += "\\usepackage[T1]{fontenc}\n"
                    preamble += "\\usepackage{fontspec}\n"
                    preamble += "\\pagenumbering{gobble}"
                    preamble += "\\begin{document}\n"
                    postamble = "\\end{document}"
                    f.write(preamble)
                    f.write(latex_str)
                    f.write(postamble)