import os
import pandas as pd
import folium
import osmnx as ox
import geopandas as gpd
import datetime

######################## Get most recent Peaks_List
# Define the place (Bavarian Forest) using its name
place_name = "Bayerischer Wald"
# Download the points of interest (peaks) within the Bavarian Forest area
tags = {'natural': 'peak'}
gdf = ox.features_from_place(place_name, tags, which_result=2)  # Adjust the which_result parameter as needed
# Filter peaks with names
peaks_with_names = gdf[~gdf['name'].isnull()]
# Extract required columns (name, elevation, latitude, longitude)
peaks_data = peaks_with_names[['name', 'ele', 'geometry']].copy()
# Extract latitude and longitude from geometry
peaks_data['latitude'] = peaks_data['geometry'].y
peaks_data['longitude'] = peaks_data['geometry'].x
# Drop the geometry column
peaks_data.drop(columns=['geometry'], inplace=True)
# Get today's date in the format 'YYMMDD'
today_date = datetime.datetime.now().strftime('%y%m%d')
# Define the file name with today's date
file_name = f'peaks_raw_data_{today_date}.csv'
# Export the DataFrame to a CSV file with today's date in the file name and including the index
peaks_data.to_csv(file_name, index=False)


################# Make Peaks Map
# Import Peaks from the CSV file
imported_peaks_data = pd.read_csv("peaks_data.csv")
# Define color palette
color_palette = {"old": "navy", "new": "firebrick", "planned": "purple"}
# Create Map
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
map_peaks.save('/Users/stefandillinger/Nextcloud/Daten/Training/peaks_progress.html')