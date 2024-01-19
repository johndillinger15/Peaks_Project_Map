import os
import pandas as pd
import folium
from datetime import datetime

# Import Peaks from the CSV file
imported_peaks_data = pd.read_csv("peaks_data.csv")

# Define color palette
color_palette = {"old": "red", "new": "navy", "planned": "purple"}

# Create folium map
# map_center = [48.9, 12.9]
# map_zoom = 9

map_peaks = folium.Map(tiles='openstreetmap')

# Add circle markers to the map
for index, row in imported_peaks_data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        popup=f"{row['name']}<br> Elevation: {row['elevation']}m, <br>Gelaufen:, {row['gelaufen']}",
        color=color_palette[row['type']],
        fill=True,
        fill_opacity=0.75,
        radius=10
    ).add_to(map_peaks)

# Fit the map to include all circle markers
map_peaks.fit_bounds(map_peaks.get_bounds())

# Display the map
map_peaks
current_date = datetime.now().strftime("%Y%m%d")
file_name_html = f"peaks_progress_{current_date}.html"
map_peaks.save(file_name_html)