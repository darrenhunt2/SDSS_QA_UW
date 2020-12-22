"""fiberSort.py

Previously called : brightline1d.py
Author : Darren Hunt, University of Washington
Adapted from IDL code written by : Nathan De Lee, NKU
Edited by : Jennifer Sobeck, University of Washington

Usage : run from command line
fibersort.py "<ref.fits>" <filepattern>

To run plotter :
fibersort.py "<ref.fits>" <filepattern> <testout.csv>

For details, see fiberSort.md
"""

import sys
import glob
import numpy as np
from astropy.io import fits
from astropy.time import Time
import matplotlib.pyplot as plt

class FiberSort:
    """
    A class for comparing a reference flat image with a set of flats or sciences to
    determine a decrease in brightness and performance. APOGEE-2 images have 300
    total fibers. Use with 1D images.

    Attributes
    ----------
    ref : str
        String of the master/reference fits flat file name
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

        # check if user input files not found
        if len(glob.glob(self.ref)) < 1:
            sys.exit("No reference flat found.")
        elif len(glob.glob(self.filepattern)) < 1:
            sys.exit("No files found.")

    def main(self):
        """
        The fibersort function takes in a reference flat image where all 300 fibers are detected,
        and compares it to a set of science or flat images for a decrease in brightness. Prints flux output
        to a .csv file named after the exposure number.

        The ratio of the fiber flux to the reference fiber flux is used to determine if a fiber is missing,
        faint, or performing as expected :

        Ratio < 0.3 : fiber is missing
        Ratio >= 0.3 and < 0.7 : fiber is faint
        Ratio >= 0.7 : fiber is good

        Returns
        -------
        r : float
            Array containing ratio values for 300 fibers
        """

        files = glob.glob(self.filepattern)
        refimage = fits.getdata(self.ref).astype(np.int32)
        r = []
        for i in range(len(files)):  # repeat for each input image
            img = fits.getdata(files[i]).astype(np.int32)
            missingFarray, faintFarray, ratarr = [], [], []
            ff = open(str(files[i][5:15])+".csv", 'w')  # file to write flux ratio values to

            for j in range(300):  # 300 fibers per image
                # fibers are reversed in 1d images compared to raw images
                flux = np.median(img[299-j,:])
                refflux = np.median(refimage[299-j,:])
                # compares input img flux to master flat flux for the same fiber
                ratio = flux / refflux

                # write to csv file
                ff.write(str(ratio)+"\n" if j < 299 else str(ratio))

                # classify fibers as missing or faint
                if ratio < 0.2:
                    missingFarray.append(int(j+1))
                elif (ratio >= 0.2) and (ratio < 0.7):
                    faintFarray.append(int(j+1))
                ratarr.append(ratio)
            # return fluxes to use in plotter function
            r.append(ratarr)
            # print array of faint and missing fibers
            with open(str(files[i][5:15])+".txt", 'w') as o:
                o.write(str(missingFarray)+";"+str(faintFarray))

        return np.asarray(r)
        o.close(), ff.close()

    def flux_plotter(self,testout):
        """
        Scatterplots the calculated 1D flux ratio for all 300 fibers, against fluxes from an external .csv file.
        The testout csv file should be flux output from raw calculations (mountain code) for comparison.
        For multiple input comparison images, the testout.csv files must use the same exposures.

        Saves a figure for each image in the input filepattern.
        Fibers above a flux ratio of 2.0 are not significant and are cut off from the plot.
        """

        plt.style.use('ggplot')
        ims = glob.glob(self.filepattern)
        o = glob.glob(testout)
        x = np.arange(1,301,1)  # x vals array for plotting. main and input csv provide the y vals
        r = self.main()

        # check there are equal number of csv files to input fits imgs for plotting
        if len(o) != len(ims):
            sys.exit("Error: incorrect number of csv files. Provide "+str(len(ims))+" csv files for plotting")

        # plot a figure for each input image in filepattern
        for i in range(len(ims)):
            # read in csv data. assumes a single flux value per line.
            mtn = np.genfromtxt(o[i],dtype='float',delimiter='\n')
            fitsim = fits.getheader(ims[i])
            flux = r[i]

            plate = fitsim['PLATEID']
            t = int(np.around(Time(fitsim['DATE-OBS']).mjd))

            fig, ax = plt.subplots(1,1,figsize=(12,12))
            ax.set_title("Fiber Flux Comparison \n Plate "+str(plate)+" , MJD "+str(t),fontsize=24)
            ax.set_xlabel("Fiber No.",fontsize=18), ax.set_ylabel("Flux Ratio",fontsize=18)
            ax.tick_params(labelsize=16), ax.set_ylim(-0.1,2)  # cut off anything above a flux ratio of 2

            ax.scatter(x,mtn,marker='s',label='Mountain output, raw imgs',color='b')  # raw image/mountain output
            ax.scatter(x,flux,marker='o',label='fiberSort output, reduced imgs',color='r',alpha=0.6)  # this code's output from main

            # missing and faint threshold lines. any fiber below these lines is missing/faint. above=OK.
            ax.plot(x,np.full((300),0.3),linestyle='--',linewidth=3,color='black')
            plt.text(2,0.25,"Missing",fontsize=14)
            ax.plot(x,np.full((300),0.7),linestyle='--',linewidth=3,color='black')
            plt.text(2,0.65,"Faint",fontsize=14)

            ax.legend(loc='best',fontsize=18)
            plt.savefig((str(ims[i][5:15])+".png"),dpi=300,overwrite=True)

if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) == 2:
        sys.exit("Error : no input files")
    r,f  = str(sys.argv[1]), str(sys.argv[2])
    FiberSort(r,f).file_check()
    FiberSort(r,f).main()
    if len(sys.argv) == 4:  # run plotter function
        t = sys.argv[3]
        FiberSort(r,f).flux_plotter(t)
    if len(sys.argv) > 4:
        sys.exit("Error : too many inputs. Usage : fibersort.py <'ref.fits>' <filepattern> optional:<testout.csv>")
