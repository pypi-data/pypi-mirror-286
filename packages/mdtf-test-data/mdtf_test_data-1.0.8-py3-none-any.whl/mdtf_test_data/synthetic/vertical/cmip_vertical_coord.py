""" Module for generating synthetic CMIP datasets """

___all__ = [
    "cmip_vertical_coord",
]

import xarray as xr
import numpy as np


def cmip_vertical_coord():
    """Generates generic CMIP6 vertical pressure coordinate

    Returns
    -------
    xarray.DataArray
        CMIP6 pressure levels
    """

    plev = np.array(
        [
            10,
            20,
            30,
            50,
            70,
            100,
            125,
            150,
            175,
            200,
            225,
            250,
            275,
            300,
            350,
            400,
            450,
            500,
            550,
            600,
            650,
            700,
            750,
            800,
            825,
            850,
            875,
            900,
            925,
            950,
            975,
            1000
        ]
    )

    plev_attrs = {
        "long_name": "air_pressure",
        "units": "hPa",
        "cartesian_axis": "Z",
        "positive": "down"
    }


    dset_out = xr.Dataset()
    dset_out["plev"] = xr.DataArray(
        plev, dims={"plev": plev}, coords={"plev": plev}, attrs=plev_attrs
    )

    return dset_out
