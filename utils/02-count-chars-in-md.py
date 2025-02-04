import os
import shutil
import pandas as pd

# Define input and output directories
input_dir = 'data/markdown/'
backup_dir = 'data/markdown_long/'
output_dir = 'data/temp/'
output_file = 'character_count.xlsx'

# OpenAI API token limit and buffer
MAX_TOKEN_LIMIT = 128000
TOKEN_BUFFER = 10000
ADJUSTED_TOKEN_LIMIT = MAX_TOKEN_LIMIT - TOKEN_BUFFER

# Approximate number of characters per token
CHARS_PER_TOKEN = 4

# Create the backup and output directories if they don't exist
os.makedirs(backup_dir, exist_ok=True)
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
                
                # Estimate token count
                estimated_tokens = char_count / CHARS_PER_TOKEN
                
                # Backup the original file
                shutil.copy(file_path, os.path.join(backup_dir, filename))
                
                # Trim content if it exceeds the adjusted token limit
                if estimated_tokens > ADJUSTED_TOKEN_LIMIT:
                    # Calculate the maximum number of characters allowed
                    max_chars = ADJUSTED_TOKEN_LIMIT * CHARS_PER_TOKEN
                    # Trim the content
                    content = content[:int(max_chars)]
                    # Save the trimmed content back to the original file
                    with open(file_path, 'w', encoding='utf-8') as md_file:
                        md_file.write(content)
                    char_count = len(content)  # Update character count after trimming
                    estimated_tokens = char_count / CHARS_PER_TOKEN  # Update token estimate
                
                # Append the result to the list
                char_counts.append({
                    'Filename': filename, 
                    'Character Count': char_count, 
                    'Estimated Tokens': estimated_tokens
                })

        except Exception as e:
            print(f"Failed to process '{filename}': {e}")

# Create a DataFrame from the collected data
char_counts_df = pd.DataFrame(char_counts)

# Save the DataFrame to an Excel file
output_path = os.path.join(output_dir, output_file)
char_counts_df.to_excel(output_path, index=False)

print(f"Character counts and estimated token counts saved to '{output_path}'")
