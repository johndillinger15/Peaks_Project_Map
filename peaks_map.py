import os
import pandas as pd
import folium
from datetime import datetime

# Import Peaks from the CSV file
imported_peaks_data = pd.read_csv("peaks_data.csv")

# Define color palette
color_palette = {"old": "navy", "new": "red", "planned": "purple"}

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

# Save the map
map_peaks.save('peaks_progress.html')
