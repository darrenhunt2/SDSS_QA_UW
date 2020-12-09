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
    A class for

    Attributes
    ----------
    ref : str
        String of the master fits flat file name
    filepattern : str
        String of similarly named fits files for comparison to ref flat and

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
        The brighline1d function

        Returns
        -------
        missingFarray :
            Array of fibers with ratio less than 0.3 compared to master flat
        faintFarray :
            Array of fibers with ratio between 0.3 and 0.7 compared to master flat
        goodFarray :
            Array of fibers with ratio above 0.7 compared to the master flat
        """

        # files to write percent differences, ratios, and mtp perdiffs and ratios to
        fib_per = open('fiber_per.out', 'w')
        fib_ratio = open('fiber_ratio.out', 'w')
        fib_mtp = open('fiber_mtp.out', 'w')

        files = glob.glob(self.filepattern)
        refimage = fits.getdata(self.ref).astype(np.int32)
        # exception if user input files not found
        if len(files) < 1:
            sys.exit("No files found.")
        elif len([refimage]) < 1:
            sys.exit("No reference flat found.")

        for i in range(len(files)):
            img = fits.getdata(files[i]).astype(np.int32)

            out = open("output.out", 'w')  # machine readable
            txt = open("output.txt", 'w')  # text version
            for j in range(300):
                flux = np.median(img[299-j,:])   # fibers are reversed in 1d images
                                                    # compared to raw images
                refflux = np.median(refimage[299-j,:])
                ratio[j] = flux[j] / refflux[j]    # compares input img flux to
                                                # master flat flux for the same fiber
                # calculate percent difference from reference
                perdiff = (flux[j] - refflux[j]) / refflux[j] * 100

                out.write(flux[j], refflux[j], ratio[j], perdiff[j])
                txt.write("Fiber no. {}; flux : {}, refflux : {}, ratio : {}, perdiff : {}".format(j,
                            flux[j], refflux[j], ratio[j], perdiff[j])+"/")
                txt.close(), out.close()

                # classify fibers as missing, faint, or good based on flux
                if ratio[j] < 0.2:
                    missingFarray = (int(j+1))
                elif (ratio[j] >= 0.2) and (ratio[j] < 0.7):
                    faintFarray = (int(j+1))
                else:
                    goodFarray = int(j+1)

                sortmin = np.sort(flux)
                print("Three Lowest Flux Fibers: ", filelist[i])
                for k in range(3):
                    print(sortmin[k]+1, ":", flux[sortmin[0]])

                print("Median Ratio", np.median(ratio))
                print("Median Percent Difference", np.median(perdiff))
                print("Median Ratio Percent Difference")
                for k in range(0, 9):
                    mtpratio[k] = np.median(ratio[0 + 30 * k:29 + 30 * k])
                    mtpdiff[k] = np.median(perdiff[0 + 30 * k:29 + 30 * k])
                    k = k + 1
                    print("MTP:", mtpratio[k], mtpdiff[k])

                # print machine readable output file
                fib_per.write(filelist[i], ratio)
                fib_ratio.write(filelist[i], perdiff)
                fib_mtp.write(filelist[i], mtpratio, mtpdiff)

                return missingFarray, faintFarray, goodFarray
        fib_per.close()
        fib_ratio.close()
        fib_mtp.close()

if __name__ == "__main__":
    r,f  = str(sys.argv[1]), str(sys.argv[2])
    Brightline(r,f).file_check()
    Brightline(r,f).main()
