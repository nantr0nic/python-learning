import json
from pathlib import Path

import plotly.express as px

# Read data as a string and conver to a Python object
try:
    path = Path("eq_data/eq_data_30_day_m1.geojson")
    contents = path.read_text()
    all_eq_data = json.loads(contents)
except FileNotFoundError:
    print("The data file was not found.")
    all_eq_data = None
except json.JSONDecodeError:
    print("The data file is not a valid JSON file.")
    all_eq_data = None
except Exception as e:
    print(f"An error occurred while reading the data: {e}")
    all_eq_data = None

all_eq_dicts = all_eq_data["features"] if all_eq_data else []

mags, lons, lats, eq_titles = [], [], [], []
for eq_dict in all_eq_dicts:
    try:
        mag = eq_dict["properties"]["mag"]
        lon = eq_dict["geometry"]["coordinates"][0]
        lat = eq_dict["geometry"]["coordinates"][1]
        title = eq_dict["properties"]["title"]
        mags.append(mag)
        lons.append(lon)
        lats.append(lat)
        eq_titles.append(title)
    except KeyError as e:
        print(f"Missing key: {e}\nSkipping...")
        continue
    except TypeError as e:
        print(f"Type error: {e}\nSkipping...")
        continue

title = "Global Earthquake Map"
fig = px.scatter_geo(
    lat=lats,
    lon=lons,
    size=mags,
    title=title,
    color=mags,
    color_continuous_scale="Viridis",
    labels={"color": "Magnitude"},
    projection="natural earth",
    hover_name=eq_titles,
)

try:
    fig.write_html("eq_world_map.html")
except OSError as e:
    print(f"An error occurred while writing the HTML file: {e}")
