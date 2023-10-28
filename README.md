# Pround

This package provides the functionality to create excel and LaTeX tables with some measured data. If the measured data has error the values are rounded accordingly (see [rounding](#Rounding)).

## Requirements

This package uses different external packages that need to be installed:

- [numpy](https://numpy.org) ([License](https://numpy.org/doc/stable/license.html))
- [pandas](https://pandas.pydata.org) ([License](https://github.com/pandas-dev/pandas/blob/main/LICENSE))
- [uncertainties](https://pythonhosted.org/uncertainties/) ([License](https://pythonhosted.org/uncertainties/#license))

All can be installed with `pip`:

```bash
pip install numpy pandas uncertainties
```

## Usage

There are a few examples in the [examples] folder. 

## Rounding

This package uses the uncertainties package, so the rounding that is used there is also used here (should be rounding up at 5 and above). If a data point has an error the error is rounded at the first significant digit, except this is a 1 or 2, then one digit after that (maximal 2 digits). The value is rounded at the same precision as the error. 
