import numpy as np
import pandas as pd
import pydeck as pdk

df = pd.read_csv("data/temp_budapest.tsv", sep="\t")
df.fillna(0, inplace=True)
levels = ["l6", "l7", "l8"]

for level in levels:
    print(level)
    df2 = df.groupby(level).mean()
    df2.reset_index(inplace=True, level=[level])
    df2["rescaled"] = [255 - ((e**3)/100) for e in df2["celsius"]]
    layer = pdk.Layer(
        "H3HexagonLayer",
        df2,
        get_hexagon=level,
        auto_highlight=True,
        pickable=True,
        extruded=True,
        coverage=0.8,
        opacity=0.05,
        get_fill_color="[255, rescaled, 0]",
    )

    view_state = pdk.ViewState(
        latitude=47.500000, longitude=19.040236, zoom=10.5, bearing=0, pitch=35
    )
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "temperature (celsius): {celsius}"},
    )
    r.to_html(f"vizs/temperature_{level}.html")
