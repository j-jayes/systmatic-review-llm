import os
import pandas as pd

# Define input and output directories
input_dir = 'data/markdown/'
output_dir = 'data/temp/'
output_file = 'character_count.xlsx'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# List to store character count data
char_counts = []

# Iterate over all Markdown files in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith('.md'):
        file_path = os.path.join(input_dir, filename)
        
        try:
            # Read the content of the Markdown file
            with open(file_path, 'r', encoding='utf-8') as md_file:
                content = md_file.read()
                char_count = len(content)
                
                # Append the result to the list
                char_counts.append({'Filename': filename, 'Character Count': char_count})

        except Exception as e:
            print(f"Failed to read '{filename}': {e}")

# Create a DataFrame from the collected data
char_counts_df = pd.DataFrame(char_counts)

# Save the DataFrame to an Excel file
output_path = os.path.join(output_dir, output_file)
char_counts_df.to_excel(output_path, index=False)

print(f"Character counts saved to '{output_path}'")
