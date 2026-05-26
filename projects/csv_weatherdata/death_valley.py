import csv
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

weather_file: str = "death_valley_2021_simple.csv"

try:
    lines: list[str] = Path("weather_data/" + weather_file).read_text().splitlines()
except FileNotFoundError:
    print(f"{weather_file} not found in weather_data/. Aborting.")
    exit()

reader = csv.reader(lines)
header_row = next(reader)

for index, column_header in enumerate(header_row):
    print(index, column_header)

dates = []
highs: list[int] = []
lows: list[int] = []

for row in reader:
    try:
        current_date = datetime.strptime(row[2], "%Y-%m-%d")
        high = int(row[3])
        low = int(row[4])
    except ValueError:
        print(f"Missing data for {current_date}. Skipping.")
        continue
    else:
        dates.append(current_date)
        highs.append(high)
        lows.append(low)

# Plot the high and low temperatures
plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots()
ax.plot(dates, highs, color="red", alpha=0.6)
ax.plot(dates, lows, color="blue", alpha=0.6)
ax.fill_between(dates, highs, lows, facecolor="blue", alpha=0.1)

# Format the plot
ax.set_title("Daily High and Low Temperatures, 2021\nDeath Valley, CA", fontsize=20)
ax.set_xlabel("", fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel("Temperature (F)", fontsize=16)
ax.tick_params(labelsize=16)

plt.show()
