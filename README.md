# SDSS APOGEE-2S Fiber Performance QA

A quality assurance project examining fiber underperformance for SDSS-IV's APOGEE-2S.

## Contents

- fiberSort -- a Python script to compare nightly flat fiber fluxes to a reference flat with an end goal of determining which fibers are missing or faint from an exposure. The output from code run for raw images is compared to fiberSort, which calculates fiber flux after data processing. For details, see fiberSort.md.

- convertfits -- two Python scripts, convertfits.py and colchecker.py. convertfits takes pixel values along a single column and converts it into a .dat for the purpose of simplifying working with multidimensional arrays. colchecker examines pixel intensity values across 5 randomly selected columns from the reference flat. For details, see convertinfo.md.

- plots -- sample output plots from fiberSort using the test images provided in the fiberSort folder.

- vignetting -- html report of vignetting at LCO and what the start of a project examining vignetting could potentially look like.

- old -- outdated code.

## Plate 11899

We selected plate 11899, a field examining the galactic halo, for test plate to work with in fiberSort. We use exposures from four MJDS (58708, 58714, 58769, 58800) to examine fiber performance on four different observing dates using the same plate. This plate was chosen to start small while working out the logistics of our code. MJD 58800 displayed typical data, with no obvious bad exposures or several fibers classified as faint and missing from the raw flux calculations.
