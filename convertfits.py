""".fits to .dat converter
This script will convert values along a specified column of a fits file into
a .dat file of values.

Run from command line:
convertfits.py "flatname.fits"

The default column for the SDSS master flat is 2952. This column can be changed
by specifying a different integer at the command line.

Author: Darren Hunt, University of Washington
"""

import sys
import numpy as np
from astropy.io import fits

class Converter:
    """
    A class for fits conversion and manipulation.

    Attributes
    ----------
    f : str
        Full name of the flat file to convert, must be a .fits file
    col : int
        Columm to pull data from. For SDSS master flat, col=2952
    """

    def __init__(self,f,col=None):
        self.f = f
        if col == None:
            self.col = 2952
        else: self.col = col

    def main(self):
        """Prints to a .dat file with values along specified column

        Parameters
        ----------
        f : str
            Full name of the flat file to convert, must be a .fits file
        col : int (optional, default=2952)
            Columm to pull data from. For SDSS master flat, col=2952
        """

        flat = fits.getdata(self.f)  # retrieve data from input fits image
        w = flat.shape[0]  # get width of chip from the image size
        out = open((self.f.rsplit('.',1)[0]+".dat"), 'w')  # name output file after input flat string, without .fits ext

        for i in range(w):
            data = flat[(w-1)-i,self.col]  # pulls the relevant value along specified column for each pixel on the chip
            decimal = '{:.18e}'.format(data)  # converts to a decimal format to 18 places before writing to .dat
            out.write(decimal + str("\n"))
        out.close()

    def equivalency(self,m):
        """Compares .dat files for equivalency, can be used to determine if
            there is user error in col parameter input. Converts all values to integers
            for comparison.

        Parameters
        ----------
        m : str
            Master .dat file to compare new .dat file values to
        """
        # replace the file extension from .fits to .dat
        valf = np.float64(np.loadtxt(self.f.rsplit('.',1)[0]+str(".dat")))
        valm = np.float64(np.loadtxt(m))
        print((valf == valm).all())

if __name__ == "__main__":
    f = str(sys.argv[1])
    if len(sys.argv) == 4:  # only if running equivalency function
        c = int(sys.argv[2])
        m = str(sys.argv[3])
        Converter(f,c).equivalency(m)
    elif len(sys.argv) == 3:  # if running with non-default column
        c = int(sys.argv[2])
        Converter(f,c).main()
    else:  # run with default column setting
        Converter(f,None).main()
