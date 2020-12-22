"""brightine 1d

Author : Darren Hunt, University of Washington
Adapted from IDL code written by : Nathan De Lee, NKU

Usage : run from command line
brightline1d.py "ref.fits" filepattern

For details, see blinfo.md
"""

import sys
import glob  # gathering images
import numpy as np
from astropy.io import fits

class Brightline:
    """
    A class for comparing a reference flat image to a set of flats or sciences to
    determine a decrease in brightness and performance.

    Attributes
    ----------
    ref : str
        String of the master fits flat file name
    filepattern : str
        String of similarly named fits files for comparison to ref flat

    """

    def __init__(self,ref,filepattern):
        self.ref = ref  # reference fits image is the master flat
        self.filepattern = filepattern

    def file_check(self):
        """Checks that filepattern contains fits files only"""
        if self.filepattern.endswith(".fits"):
            pass
        else: sys.exit("Error : All files must be .fits only")

    def main(self):
        """
        The brighline1d function takes in a reference flat image such as a master
        flat where all fibers are detected, and compares it to a set of science or
        flat images for a decrease in brightness. The ratio of the fiber flux to the
        reference fiber flux is used to determine if a fiber is missing, faint, or
        performing as expected.

        Ratio < 3 : fiber is missing
        Ratio >= 3 and < 0.7 : fiber is faint
        Ratio > 0.7 : fiber is good

        Returns
        -------
        missingFarray : int arr
            Array of fibers with ratio less than 0.3 compared to master flat
        faintFarray : int arr
            Array of fibers with ratio between 0.3 and 0.7 compared to master flat
        goodFarray : int arr
            Array of fibers with ratio above 0.7 compared to the master flat
        """

        files = glob.glob(self.filepattern)
        refimage = fits.getdata(self.ref).astype(np.int32)
        # error if user input files not found
        if len(files) < 1:
            sys.exit("No files found.")
        elif len([refimage]) < 1:
            sys.exit("No reference flat found.")

        for i in range(len(files)):
            img = fits.getdata(files[i]).astype(np.int32)

            fib = open("fibers.txt", 'w')  # text file of all fibers classified by brightness ratio
            txt = open("output.txt", 'w')  # text file of all fiber details
            for j in range(300):
                # fibers are reversed in 1d images compared to raw images
                flux = np.median(img[299-j,:])
                refflux = np.median(refimage[299-j,:])

                # compares input img flux to master flat flux for the same fiber
                ratio = flux / refflux
                # calculate percent difference from reference
                perdiff = ((flux - refflux) / refflux) * 100

                txt.write("Fiber no. {}; flux : {}, refflux : {}, ratio : {}, perdiff : {}".format(j,
                            flux, refflux, ratio, perdiff)+"\n")

            # classify fibers as missing, faint, or good based on flux
            if ratio < 0.2:
                missingFarray = (int(j+1))
            elif (ratio >= 0.2) and (ratio < 0.7):
                faintFarray = (int(j+1))
            else:
                goodFarray = int(j+1)

            print("Median Ratio ", j, np.median(ratio))
            print("Median Percent Difference ", j, np.median(perdiff))

            fib.write("Missing : "+str(missingFarray)+"\n Faint : "+str(faintFarray)+"\n Good : "+str(goodFarray))
            return missingFarray, faintFarray, goodFarray
        fib.close(), txt.close()

if __name__ == "__main__":
    r,f  = str(sys.argv[1]), str(sys.argv[2])
    Brightline(r,f).file_check()
    Brightline(r,f).main()
