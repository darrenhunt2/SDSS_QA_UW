"""colchecker.py
Graphically inspect distribution of pixel intensity values for 5 randomly
selected columns across the master flat.

Usage : run from command line
colchecker.py

Author : Darren Hunt, University of Washington
Edited by : Jennifer Sobeck, University of Washington

For details, see convertinfo.md
"""

import sys
import numpy as np
from astropy.io import fits  # open and read fits data
import matplotlib.pyplot as plt

class ColumnCheck:
    """Line plots all values along 5 randomly selected columns in a flat image for visual comparison.

    Parameters
    ----------
    f : str, optional
        Name of flat file. Default is the raw master flat, exp 24960049
    """
    def __init__(self,f="asRaw-24960049.fits"):
        self.f = f

    def main(self):
        """Main plotter"""

        flat = fits.getdata(self.f)  # intensity vals

        plt.style.use('ggplot')
        fig, ax = plt.subplots(1,1,figsize=(18,12))
        ax.set_title("Pixel values (5 random columns), "+self.f.rsplit('.',1)[0],fontsize=20)
        ax.set_xlabel("Pixel",fontsize=16), ax.set_ylabel("Intensity",fontsize=16)
        ax.tick_params(labelsize=14)

        x = np.arange(0,2048,1)  # number of pix in a single col
        #y = [[(np.random.randint(0,8192,size=5))]]
        y = []
        for i in range(5):
            r = np.random.randint(0,8192,size=1)
            data = flat[0:2048, r]  # grab pixel values for each random column
            y.append([r,data])

        ax.scatter(x,y[0][1],color='red',label=y[0][0])
        ax.scatter(x,y[1][1],color='blue',alpha=0.9,label=y[1][0])
        ax.scatter(x,y[2][1],color='green',alpha=0.7,label=y[2][0])
        ax.scatter(x,y[3][1],color='orange',alpha=0.6,label=y[3][0])
        ax.scatter(x,y[4][1],color='magenta',alpha=0.5,label=y[4][0])

        ax.legend(loc='upper left',title="column no.",fontsize=14)
        plt.savefig(str(self.f.rsplit('.',1)[0])+".png",dpi=300,overwrite=True)

if __name__ == "__main__":
    if len(sys.argv) > 2 :
        sys.exit("Error : too many inputs")
    elif len(sys.argv) == 2:  # read user input file
        f = sys.argv[1]
        ColumnCheck(f).main()
    else:
        ColumnCheck().main()
