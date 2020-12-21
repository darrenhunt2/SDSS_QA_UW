# Convertfits.py

.fits to .dat converter along a specified column of a fits image.

Author : Darren Hunt, University of Washington

Edited by : Jennifer Sobeck, SDSS-IV Project Manager for APOGEE-2 and LCO Operations, University of Washington

## Purpose

The Sloan Digital Sky Survey (SDSS-IV) is a dual-hemisphere astronomical survey studying all aspects of the Milky Way galaxy. Unlike most other telescopes, the SDSS has the unique ability to observe multiple objects at once. This is achieved by using plug plates, specially-machined circular plates with 300 precisely drilled holes where light-collecting fibers plug in. Three types of fibers collect data while observing: target (250 fibers), telluric calibration to subtract atmospheric effects (15 fibers), and sky calibration (35 fibers).

APOGEE-2, or the second generation Apache Point Observatory Galaxy Evolution Experiment, is a high resolution (R ~ 22,500), near-infrared (wavelength range: 1.51-1.70 micrometers) spectrograph at the northern Apache Point Observatory (APO) in New Mexico. Las Campanas Observatory (LCO) in Chile has a duplicated version of this spectrograph. APOGEE-2 focuses on the evolution of the galaxy, such as star formation, age, and dynamics of the galaxy.

This overall scope of this project aims to determine which fibers at the LCO telescope have continuous poor performance over time. Poor performance can result from human error such as a loose fiber connection, deterioration from use over time, or poor performance since commissioning. This code's role in the quality assurance of LCO fibers is to simplify working with multidimensional array data in flat images. .fits files can store multiple types of data values along different dimensions, spatial and spectral. The size of the spatial pixel value array is (2048,8192) rows and columns for SDSS images. Converting from .fits to .dat simplifies working with the flat data by reducing the number of array dimensions down to one. Accessing a specific column is more cumbersome otherwise.

### Column default : 2952

Dome flat sequences of a uniformly illuminated field of view are taken periodically while observing. The current master flat for the south, asRaw-24960049.fits, is used as a baseline for comparison, as all 300 fibers were picked up.

Although in convertfits.py there is an option to input a specified column, the default is set to 2952. This column is uniquely chosen for the current master flat. This column is likely selected based on its spatial location: away from pixels on the image edges, and away from any chip gaps. The spectrograph CCD has an R, G, and B chip for a total of three observational detectors with small gaps in between each, and 3 additional 512x2048 reference chips to identify any instrument errors. (Nidever et al., 2015) Avoiding the gaps reduces any zero or atypical pixel values.

See colchecker.py code for a visual comparison of randomly selected columns across a flat image.

### colchecker.py and .ipynb

colchecker runs similarly to convertfits.py, but pulls data along a column to plot it and does not print to an output file. Using the master flat, colchecker plots the values of the 2048 pixels along randomly selected columns across the image within a range of (0,8192). Currently, 5 random columns are plotted at a time per figure, in addition to the line for column 2952.

The values across the image's columns follow a general trend (pix value around ~2000), and outliers of very high values deviating above the average, or negative values dipping far below, display visible spikes across the plot. This helps determine which columns are ideal (or not) to use as reference values if they stray too far from the expected value range.

## Usage

To convert the default column 2952 from a flat image into a .dat file, run from the command line:

convertfits.py <"flatexp.fits">

To convert all values along any one column in the range of (0,8192) for SDSS images, run from the command line:

convertfits.py <"flatexp.fits"> <col>

### Value checker function

The value_checker function compares every line in a .dat file to another for equivalency. This does not run by default, but can be used to double check that all values match an existing .dat file. To use the value_checker, run from the command line:

convertfits.py <"flat.dat"> <col> <"mastercol.dat">

### Future improvements

- Improved command line interaction with exceptions and user prompts to input correct file type (.fits or .dat) and to provide a column value only within the range of the input image.
- Fix value_checker to run without specifying column number, currently cannot run without specifying all three input parameters.

## Citations

1. APOGEE-2 | APO Galactic Evolution Experiment 2. (n.d.). Retrieved from https://www.sdss.org/surveys/apogee-2/

2. Nidever, D. L. et al. (2015). The Data Reduction Pipeline for the Apache Point Observatory Galactic Evolution Experiment. The Astronomical Journal, 150(6). doi:10.1088/0004-6256/150/6/173
