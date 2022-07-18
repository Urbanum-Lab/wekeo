import os

import h3
import pandas as pd
import xarray as xr

df6 = pd.read_csv("data/aggregated/l6.tsv", sep="\t")
df7 = pd.read_csv("data/aggregated/l7.tsv", sep="\t")
df8 = pd.read_csv("data/aggregated/l8.tsv", sep="\t")

h3_l6 = set(df6["l6"])
h3_l7 = set(df7["l7"])
h3_l8 = set(df8["l8"])

root_folder = "data/leaf_data"
fs = [
    os.path.join(root_folder, f)
    for f in os.listdir(root_folder)
    if os.path.isfile(os.path.join(root_folder, f))
]

ll2lai = {}

for f in fs:
    try:
        print(f)
        ds = xr.open_dataset(filename_or_obj=os.path.join(f), engine="netcdf4")
        lat = ds.data_vars["LAI"]["lat"].to_numpy()
        lat = [e for e in lat if 47.392134 < e < 47.601216]
        lon = ds.data_vars["LAI"]["lon"].to_numpy()
        lon = [e for e in lon if 18.936234 < e < 19.250031]
        time = ds.data_vars["LAI"]["time"].to_numpy()[0]
        for i in range(len(lat)):
            for j in range(len(lon)):
                one_point = ds["LAI"].sel(lat=lat[i], lon=lon[i])
                vals = one_point.values[0]
                if ll2lai.get((lat[i], lon[j]), False):
                    ll2lai[(lat[i], lon[j])] = (ll2lai[(lat[i], lon[j])] + vals) / 2.0
                else:
                    ll2lai[(lat[i], lon[j])] = vals
    except Exception as exc1:
        print("outer exception", exc1)
        continue

with open("data/lai_budapest.tsv", "w") as outfile:
    h = "lat\tlong\tlai\tl6\tl7\tl8\n"
    outfile.write(h)
    for k, v in ll2lai.items():
        h6 = h3.geo_to_h3(k[0], k[1], 6)
        h7 = h3.geo_to_h3(k[0], k[1], 7)
        h8 = h3.geo_to_h3(k[0], k[1], 8)
        if h6 in h3_l6 and h7 in h3_l7 and h8 in h3_l8:
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
