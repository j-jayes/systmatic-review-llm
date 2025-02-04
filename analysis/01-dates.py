import os
import json
import pandas as pd

# Define the directory containing the JSON files
directory = 'data/openai_output'

# Initialize a list to store the extracted data
data = []

# Loop through all JSON files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        
        with open(file_path, 'r') as file:
            try:
                content = json.load(file)
                
                # Extract the relevant information
                time_start = content.get('design', {}).get('time_period_start')
                time_end = content.get('design', {}).get('time_period_end')
                technologies = content.get('relevance', {}).get('technologies', [])
                
                # Add to the data list
                data.append({
                    # get the authors from the JSON file and concatenate them into a single string
                    'authors': ", ".join(content.get('metadata', {}).get('authors', [])),
                    'file': filename,
                    'time_period_start': time_start,
                    'time_period_end': time_end,
                    'technologies': ", ".join(technologies)
                })
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {filename}")

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('data/temp/extracted_technologies.csv', index=False)

print("Data extraction complete. CSV saved as 'extracted_technologies.csv'")
