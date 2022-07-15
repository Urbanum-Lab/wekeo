import os

import h3
import xarray as xr

root_folder = "data/temp_data"
dirs = [
    os.path.join(root_folder, d)
    for d in os.listdir(root_folder)
    if os.path.isdir(os.path.join(root_folder, d))
]


def is_within_bounding_box(lat, long):
    if 47.392134 < lat < 47.601216 and 18.936234 < long < 19.250031:
        return True
    else:
        return False


latlong_temp = {}
for inpath in dirs:
    # TODO: take all data and calculate avg tmp for the month
    # geodetic_tx.nc -> latitude_tx, longitude_tx
    geodetic = xr.open_dataset(
        filename_or_obj=os.path.join(inpath, "geodetic_tx.nc"), engine="netcdf4"
    )
    lat = geodetic.data_vars["latitude_tx"].to_numpy().flatten()
    long = geodetic.data_vars["longitude_tx"].to_numpy().flatten()
    # met_tx.nc -> temperature_tx
    met_tx = xr.open_dataset(
        filename_or_obj=os.path.join(inpath, "met_tx.nc"), engine="netcdf4"
    )
    temp = met_tx.data_vars["temperature_tx"].to_numpy().flatten()
    # LST_ancillary_ds.nc -> NDVI (empyt :()
    lst = xr.open_dataset(
        filename_or_obj=os.path.join(inpath, "LST_ancillary_ds.nc"), engine="netcdf4"
    )
    ndvi = lst.data_vars["NDVI"].to_numpy().flatten()

    temp_data = zip(lat, long, temp)
    temp_data = (e for e in temp_data if is_within_bounding_box(e[0], e[1]))
    for e in temp_data:
        k = (e[0], e[1])
        if latlong_temp.get(k, False):
            latlong_temp[k] = (latlong_temp[k] + e[2]) / 2
        else:
            latlong_temp[k] = e[2]

with open("data/temp_budapest.tsv", "w") as outfile:
    h = "lat\tlong\tcelsius\tl6\tl7\tl8\n"
    outfile.write(h)
    for k, v in latlong_temp.items():
        l6 = h3.geo_to_h3(k[0], k[1], 6)
        l7 = h3.geo_to_h3(k[0], k[1], 7)
        l8 = h3.geo_to_h3(k[0], k[1], 8)
        o = (
            str(k[0])
            + "\t"
            + str(k[1])
            + "\t"
            + str(v - 273.15)
            + "\t"
            + l6
            + "\t"
            + l7
            + "\t"
            + l8
            + "\n"
        )
        outfile.write(o)

print("we have data!!!!!!!! " * 100)
