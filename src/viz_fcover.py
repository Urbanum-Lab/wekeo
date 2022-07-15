import pandas as pd
import pydeck as pdk

df = pd.read_csv("data/fcover_budapest.tsv", sep="\t")

levels = ["l6", "l7", "l8"]

for level in levels:
    print(level)
    layer = pdk.Layer(
        "H3HexagonLayer",
        df,
        get_hexagon=level,
        auto_highlight=True,
        pickable=True,
        extruded=True,
        coverage=0.8,
        opacity=0.001,
        get_fill_color="[255 - fcover*100, 255, fcover*100]",
    )

    view_state = pdk.ViewState(
        latitude=47.500000, longitude=19.040236, zoom=10, bearing=0, pitch=35
    )
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Fraction of Vegetation Cover: {fcover}"},
    )
    r.to_html(f"vizs/fcover_{level}.html")
