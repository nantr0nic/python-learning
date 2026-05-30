import json
from pathlib import Path

# Read data as a string and conver to a Python object
try:
    path = Path("eq_data/eq_data_1_day_m1.geojson")
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

# Create a more readable version of the data file
path = Path("eq_data/readable_eq_data.geojson")
try:
    if not path.exists():
        readable_contents = json.dumps(all_eq_data, indent=4)
        path.write_text(readable_contents)
    else:
        print(f"{path.name.removeprefix('eq_data/')} already exists.")
except Exception as e:
    print(f"An error occurred: {e}")

# Examine all earthquake data
all_eq_dicts = all_eq_data["features"] if all_eq_data else []
print(f"Earthquake count in file: {len(all_eq_dicts)}")

# mags = []
# for eq_dict in all_eq_dicts:
#     mag = eq_dict["properties"]["mag"]
#    mags.append(mag)

# mags = [eq_dict["properties"]["mag"] for eq_dict in all_eq_dicts]

# We're also going to store long/lat so actually better to use
# a single for-loop iteration than 3 list comprehensions

mags, lons, lats = [], [], []
for eq_dict in all_eq_dicts:
    mag = eq_dict["properties"]["mag"]
    lon = eq_dict["geometry"]["coordinates"][0]
    lat = eq_dict["geometry"]["coordinates"][1]
    mags.append(mag)
    lons.append(lon)
    lats.append(lat)

print(f"Magnitudes: {mags[:10]}")
print(f"Lons: {lons[:10]}")
print(f"Lats: {lats[:10]}")
