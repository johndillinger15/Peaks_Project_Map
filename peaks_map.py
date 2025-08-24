import os
import pandas as pd
import json
import folium
import osmnx as ox
import geopandas as gpd
import gpxpy
from math import radians, sin, cos, sqrt, atan2

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
# Define coordinates of Straubing
straubing_coords = (48.8817, 12.5731)  # Latitude and longitude of Straubing
# Function to calculate distance between two coordinates using Haversine formula
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance
# Calculate distance from each peak to Straubing and round to 0 decimals
peaks_data['distance_to_straubing'] = peaks_data.apply(lambda row: round(haversine_distance(row['latitude'], row['longitude'], straubing_coords[0], straubing_coords[1]), 1), axis=1)
# Sort the DataFrame based on distances in ascending order
peaks_data = peaks_data.sort_values(by='distance_to_straubing')
# Define the file name with today's date
file_name = 'peaks_raw_data.csv'
file_name_excel = 'peaks_raw_data.xlsx'
# Export the DataFrame to a CSV file with today's date in the file name and including the index
peaks_data.to_csv(file_name, index=False)
peaks_data.to_csv('/Users/stefandillinger/Documents/11ty/raincastle_blog/assets/peaks_list.csv', index=False)
peaks_data.to_excel(file_name_excel, index=False)

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
        popup=f"{row['name']}<br> Elevation: {row['elevation']}m, <br>Gelaufen: {row['gelaufen']}",
        color=color_palette[row['type']],
        fill=True,
        fill_opacity=0.75,
        radius=8
    ).add_to(map_peaks)

############### Add GPX Tracks to the Map ################
gpx_folder = "./gpx/"  # Change this to your GPX file folder

# Function to parse GPX tracks
def parse_gpx(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        tracks = []
        for track in gpx.tracks:
            for segment in track.segments:
                track_points = [(point.latitude, point.longitude) for point in segment.points]
                tracks.append(track_points)
        return tracks

# Loop through GPX files and add tracks to the map
for filename in os.listdir(gpx_folder):
    if filename.endswith(".gpx"):
        file_path = os.path.join(gpx_folder, filename)
        tracks = parse_gpx(file_path)
        for track in tracks:
            folium.PolyLine(track, color="firebrick", weight=2, opacity=0.7).add_to(map_peaks)

############### Finalize Map ################
# Fit the map to include all elements
map_peaks.fit_bounds(map_peaks.get_bounds())

# Save the map
map_peaks.save('peaks_progress.html')
map_peaks.save('/Users/stefandillinger/Nextcloud/Training/peaks_progress.html')
map_peaks.save('/Users/stefandillinger/Documents/11ty/raincastle_blog/assets/peaks_progress.html')

############ JSON Files for Website
# Calculate the number of entries in the 'gelaufen' column of peaks_data dataframe
gelaufen_entries = len(imported_peaks_data['gelaufen'])
# Calculate the number of entries in peaks_raw_data dataframe
raw_data_entries = len(peaks_data)
# Create a dictionary to store the counts
counts_data = {
    "gelaufen_entries": gelaufen_entries,
    "raw_data_entries": raw_data_entries
}
# Write the counts data to a JSON file
with open('/Users/stefandillinger/Documents/11ty/raincastle_blog/content/_data/counts_data.json', 'w') as json_file:
    json.dump(counts_data, json_file)

print("Map with GPX tracks and peaks has been updated successfully.")