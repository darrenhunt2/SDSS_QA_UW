# fiberSort.py

A script to determine the flux of APOGEE-2S fibers from 1D reduced images, compare each to a baseline, and plot output against flux calculations from code run nightly at LCO using raw images (here called 'mountain code').

Author : Darren Hunt, University of Washington

Adapted from IDL code written by : Nathan De Lee, NKU

Edited by : Jennifer Sobeck, SDSS-IV Project Manager for APOGEE-2 and LCO Operations, University of Washington

## Purpose

The Sloan Digital Sky Survey (SDSS-IV), a dual-hemisphere astronomical survey studying the Milky Way galaxy, utilizes light-collecting fibers to observe multiple objects at once. fiberSort.py examines the 300 fibers used in APOGEE-2S data collection at Las Campanas Observatory for changes in flux. For more information on SDSS and APOGEE, see convertinfo.md.

### Fiber flux QA

This code examines fiber fluxes for one or more input images, with each output file and plot focusing on one MJD at a time. The long term goal is to take these nightly outputs and analyze over a given range of time to determine any decrease in performance, continuous poor performance, or lifetime poor performance since commissioning for any fiber. While examining over time, additional parameters can be included to narrow down potential causes of subpar throughput. Cart (where fibers are plugged), weather, and plate are more variables to consider.

The script run nightly at LCO, the 'mountain code', provides missing and faint fibers for the night. The full ratio calculations are required in .csv format to run with the fiberSort scatterplotter.

### Ratio calculations

fiberSort requires a single reference flat and one or more nightly dome flats to calculate flux ratios. Exposure 24960049 is the current master flat for the south. This exposure is an ideal baseline for flux comparisons, with all 300 fibers picked up.

The median value of each fiber is taken for the reference flat and each comparative flat. A ratio of flux / reference flux is taken. This ratio indicates whether there has been a change in brightness as compared to baseline : a ratio near 1.0 indicates flux is relatively consistent; a ratio above ~2.0 is discarded (not significant). Below 1.0, there are two thresholds:

r < 0.3 : fiber is missing

r >= 0.3 and < 0.7 : fiber is faint

Any r >= 0.7 and < 2.0 we consider a good fiber.

fiberSort uses 1D images (reduced spectra after flux calibration and throughput correction (Nidever et al., 2015)) while the mountain code uses raw images (pre-data reduction) taken the night of observation. We can expect minor fluctuations in flux / refflux ratios due to this correction in 1D images, but major deviations are an area to examine for quality concerns.

### Flux scatterplots

If .csv files from the mountain code are provided, the flux_plotter function will produce a scatterplot displaying flux ratio for each fiber 1-300 from both fiberSort (1D) and mountain (raw) calculations. This allows us to determine how the pre-reduced flux calculations compare to 1D calculations, and which fibers are classified as missing or faint. The mountain code and main function of fiberSort both output missing and faint fiber arrays. However, the flux ratio for the reduced images may vary just enough so that one code classifies a fiber as faint, while another does not, with the fiber's flux slightly over the cutoff point. This explains why the mountain code may determine more fibers are missing or faint than fiberSort does. Close examination near the thresholds is therefore necessary.

An example of a scatterplot for exposure 32380009-a:

![Scatterplot example](/plots/a-32380009.png)

## Usage

fiberSort.py can be run with one comparison fits flats or a series of similarly named fits files. Running the plotter is optional.

Run main sorter function from the command line:

fiberSort.py "ref.fits" "filepattern"

This writes each ratio flux to a .csv file, and a .txt file with missing and faint fiber arrays, named after each input exposure.

Run main sorter function and plotter from the command line:

fiberSort.py "ref.fits" "filepattern" "testout.csv"

Will save a .png for each exposure. Length of fits file list and length of csv file list must match.

### Error checks

fiberSort currently checks that input files are .fits only, that there is at least one comparative flat and one reference flat, and when using the plotter function, there are an equivalent number of .csv files to .fits files read in.

## Future improvements

- Optimize flux and plotter loops; currently do not run as fast as they could.

## Sources

1. Nidever, D. L. et al. (2015). The Data Reduction Pipeline for the Apache Point Observatory Galactic Evolution Experiment. The Astronomical Journal, 150(6). doi:10.1088/0004-6256/150/6/173
