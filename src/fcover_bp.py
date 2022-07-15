import os

import h3
import xarray as xr

root_folder = "data/fcover"
fs = [
    os.path.join(root_folder, f)
    for f in os.listdir(root_folder)
    if os.path.isfile(os.path.join(root_folder, f))
]


def is_within_bounding_box(lat, long):
    if 47.392134 < lat < 47.601216 and 18.936234 < long < 19.250031:
        return True
    else:
        return False


ll2fcover = {}

for f in fs:
    try:
        print(f)
        ds = xr.open_dataset(filename_or_obj=os.path.join(f), engine="netcdf4")
        lat = ds.data_vars["FCOVER"]["lat"].to_numpy()
        lat = [e for e in lat if 47.392134 < e < 47.601216]
        lon = ds.data_vars["FCOVER"]["lon"].to_numpy()
        lon = [e for e in lon if 18.936234 < e < 19.250031]
        time = ds.data_vars["FCOVER"]["time"].to_numpy()[0]
        for i in range(len(lat)):
            for j in range(len(lon)):
                one_point = ds["FCOVER"].sel(lat=lat[i], lon=lon[i])
                vals = one_point.values[0]
                if ll2fcover.get((lat[i], lon[j]), False):
                    ll2fcover[(lat[i], lon[j])] = (
                        ll2fcover[(lat[i], lon[j])] + vals
                    ) / 2.0
                else:
                    ll2fcover[(lat[i], lon[j])] = vals
    except Exception as exc1:
        print("outer exception", exc1)
        continue

with open("data/fcover_budapest.tsv", "w") as outfile:
    h = "lat\tlong\tfcover\tl6\tl7\tl8\n"
    outfile.write(h)
    for k, v in ll2fcover.items():
        h6 = h3.geo_to_h3(k[0], k[1], 6)
        h7 = h3.geo_to_h3(k[0], k[1], 7)
        h8 = h3.geo_to_h3(k[0], k[1], 8)
        o = (
            str(k[0])
            + "\t"
            + str(k[1])
            + "\t"
            + str(v)
            + "\t"
            + str(h6)
            + "\t"
            + str(h7)
            + "\t"
            + str(h8)
            + "\n"
        )
        outfile.write(o)

print("we have data!!!!! " * 100)
