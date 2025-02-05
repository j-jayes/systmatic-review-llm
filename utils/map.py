import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from collections import Counter

# List of geographical focus areas
geographical_focus = [
    "Great Britain", "Global", "American South", "Canada", "England", 
    "Cape Colony/Province, South Africa", "Delta region in the Southern United States", 
    "England", "West of England", "China", "Sweden", "United States", "Bengal, India", 
    "Western Europe", "West Germany", "Global", "Philippines", "United Kingdom", 
    "United States and Canada", "Colonial Australia", "United States", "Sweden", 
    "France", "England", "Victoria, Australia", "Great Britain", "United States", 
    "Sweden", "England", "Lancashire, Great Britain", "Cotton South, USA", 
    "United Kingdom", "Britain", "United States", 
    "Great Britain, with a focus on Lancashire and Liverpool", "United States", 
    "San Cristóbal, Bogotá, Colombia", "United States", 
    "North-East of the USSR, including Magadan Region", "United States", "United States", 
    "United Kingdom and United States", "United States", "Sweden", "British Empire", 
    "United States", "Great Britain and Northern Ireland", "New York City", 
    "Ancient Greece and Rome", "Global", "Newfoundland and Labrador", "Southern United States", 
    "San José, California", "American South", "Britain", "Canada", "London, England", 
    "Global", "United Kingdom", "Scotland", "Bulgaria", 
    "Southern United States, particularly Arkansas, Louisiana, and Mississippi", 
    "United States", "OECD countries", "British Columbia, Canada", "Netherlands", 
    "United States and Europe", "Germany", "Virolahti, Eastern Finland", "United States", 
    "Eastern and Southern Africa", "United States"
]

# Normalize and count the occurrences
focus_counter = Counter(geographical_focus)

# Load world map
gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Map common country names to geopandas names
name_mapping = {
    "United States": "United States of America",
    "Great Britain": "United Kingdom",
    "England": "United Kingdom",
    "Scotland": "United Kingdom",
    "Britain": "United Kingdom",
    "United Kingdom and United States": "United Kingdom",
    "West Germany": "Germany",
    "Bengal, India": "India",
    "Cape Colony/Province, South Africa": "South Africa",
    "Victoria, Australia": "Australia",
    "Colonial Australia": "Australia",
    "Philippines": "Philippines",
    "China": "China",
    "Sweden": "Sweden",
    "France": "France",
    "Netherlands": "Netherlands",
    "Germany": "Germany",
    "Bulgaria": "Bulgaria",
    "Eastern and Southern Africa": "South Africa",
    "British Columbia, Canada": "Canada",
    "Canada": "Canada",
    "Newfoundland and Labrador": "Canada",
    "Southern United States": "United States of America",
    "American South": "United States of America",
    "Delta region in the Southern United States": "United States of America",
    "Southern United States, particularly Arkansas, Louisiana, and Mississippi": "United States of America",
    "United States and Canada": "United States of America",
    "United States and Europe": "United States of America",
    "Global": None,  # Ignore global as it doesn't map to a specific country
    "OECD countries": None,  # Ignore as it's a group of countries
    "British Empire": None,  # Ignore as it's historical
    "Great Britain and Northern Ireland": "United Kingdom",
    "New York City": "United States of America",
    "San Cristóbal, Bogotá, Colombia": "Colombia",
    "San José, California": "United States of America",
    "North-East of the USSR, including Magadan Region": "Russia",
    "Virolahti, Eastern Finland": "Finland",
    "Western Europe": None,  # Ignore as it's a region
    "Ancient Greece and Rome": None  # Ignore as it's historical
}

# Apply mapping to count per country
country_counts = {}
for place, count in focus_counter.items():
    country = name_mapping.get(place, place)
    if country and country in gdf['name'].values:
        country_counts[country] = country_counts.get(country, 0) + count

# Merge counts with GeoDataFrame
gdf['papers_count'] = gdf['name'].map(country_counts).fillna(0)

# Plotting the map
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
gdf.plot(column='papers_count', cmap='viridis', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

# Title and remove axis
ax.set_title('Geographical Focus of Papers on Labor Displacement', fontdict={'fontsize': 20}, pad=20)
ax.set_axis_off()

# Show the plot
plt.show()
