import pandas as pd
import folium
import osmnx as ox
import geopandas as gpd
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
map_peaks.save('/Users/stefandillinger/Documents/11ty/raincastle_blog/assets/peaks_progress.html')