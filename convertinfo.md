# Convertfits.py

.fits to .dat converter along a specified column of a fits image.

Author : Darren Hunt, University of Washington

## Purpose

Flat fields in astronomy are used to correct observational images for error due to physical dust or other obstructions on the telescope optics itself, and to normalize variations in pixel brightness. Eliminating noise from the background allows for higher quality data after the full reduction process. For the Sloan Digital Sky Survey, the data are released to the public for academic, research, and personal use. The quality of the released spectral and image data sets is therefore a high priority. Observation and calibration images are recorded as .fits files.

.fits files can store multiple types of data values along different dimensions. Pixel values are read in as an array of float or integer values. The size of the pixel value array is (2048,8192) rows and columns for SDSS images.

### Column default : 2952

Although there is an option to provide a user-chosen column, the default is set to 2952. This column is chosen for the master flat currently used in the south, asRaw-24960049.fits, where are 300 fibers are detected. This column is (likely) selected based on a location determined to be ideal based on a few factors: away from pixels on the image edges, where we will see strange visual effects; away from any chip gaps (the spectrograph CCD has an R, G, and B chip for a total of three, with small gaps in between each).

See colchecker.py code and documentation for a visual comparison of randomly selected columns across a flat image.

## Usage

To convert the default column 2952 from a flat image into a .dat file, run from the command line:

convertfits.py "flatexp.fits"

To convert all values along any one column in the range of (0,8192) for SDSS images, run from the command line:

convertfits.py "flatexp.fits" col#

### Value checker function

The value_checker function compares every line in a .dat file to another for equivalency. This does not run by default, but can be used for double checking all values match an existing .dat file. To use the value_checker, run from the command line:

convertfits.py "flatexp.dat" col# "mastercol.dat"

### Future improvements

- Improved command line interaction with exceptions and user prompts to input correct file type (.fits or .dat) and to provide a column value only within the range of the input image.
- Fix value_checker to be run without specifying column number.
