[![Total alerts](https://img.shields.io/lgtm/alerts/g/jkrasting/mdtf_test_data.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jkrasting/mdtf_test_data/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/jkrasting/mdtf_test_data.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jkrasting/mdtf_test_data/context:python)

# MDTF Diagnostics Test Data Tools
Package to work with test input datasets for MDTF Diagnostics

## Overview
This package is designed to coarsen NetCDF files for generating test datasets and produce synthetic datasets on-the-fly that can be used for testing the MDTF Diagnostics package.

## Requirements
cftime
* envyaml
* numpy
* pandas
* pytest
* xarray
* xESMF

## Getting the code

The mdtf_test_data package is available on [PyPI](https://pypi.org/project/mdtf-test-data/). 

## Installation
```
mkdir mdtf_test_data && cd mdtf_test_data
pip install mdtf-test-data
```

## Usage
This package can be used to generate fully-synthetic datasets based on NCAR's
CESM2 and GFDL's CM4 model output that can be used to test the MDTF-Diagnostics package.

```
usage: mdtf_synthetic.py [-h] [-c CONVENTION] [--startyear year] [--nyears years]
[--dlat latitude resolution in degrees] [--dlon longitude resolution in degrees] [--unittest]

Required arguments:
  -c, --convention      Data convention [NCAR, CESM, GFDL, CMIP]

Optional arguments:
  -h, --help            show this help message and exit
  --startyear           start year of data [default is 1975]
  --nyears              number of years of data to generate [default is 10]
  --dlat                latitude resolution in degrees [default is 20]
  --dlon                longitude resolution in degrees [default is 20]
  --unittest............flag to run unit tests in mdtf_test_data/tests
```
To generate NCAR CESM output in a directory called `NCAR.Synthetic`:

```
mdtf_synthetic.py -c [ NCAR | CESM ] --nyears 7 
```
Note that "NCAR" and "CESM" are both valid input values that generate output files appended with "NCAR_Synthetic".

To generate GFDL CM4 output in a directory called `GFDL.Synthetic`:
```
mdtf_synthetic.py -c GFDL --nyears 10
```

To generate CMIP output in a directory called `CMIP.Synthetic`:
```
mdtf_synthetic.py -c CMIP --nyears 10
```

To coarsen an existing NetCDF file:
```
git clone https://github.com/jkrasting/mdtf_test_data.git
cd mdtf_test_data
usage: mdtf_synthetic/util/mdtf-coarsen.py [-h] [-r REGRID_METHOD] [-o OUTFILE] [-O] infile

Coarsen a NetCDF file.

Required arguments:
  infile                Path to input NetCDF file

Optional arguments:
  -h, --help            show this help message and exit
  -r REGRID_METHOD      xESMF regridding method
  -o OUTFILE, --outfile OUTFILE
                        Filename of output NetCDF file
  -O                    Overwrite existing file
```
Notes:
* The coarsening tool only supports standard grids with dimensions name `lat` and `lon` for now
* Any xESMF regrid method may be passed with the `-r` option

## Getting Help
Submit a [GitHub Issue](https://github.com/jkrasting/mdtf_test_data/issues)
