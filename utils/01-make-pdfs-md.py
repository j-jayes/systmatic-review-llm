import os
from docling.document_converter import DocumentConverter
from docling.datamodel.document import ConversionResult

# Initialize the DocumentConverter
converter = DocumentConverter()

# Define input and output directories
input_dir = 'data/pdfs/'
output_dir = 'data/markdown/'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Iterate over all files in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith('.pdf'):
        input_path = os.path.join(input_dir, filename)
        output_filename = f"{os.path.splitext(filename)[0]}.md"
        output_path = os.path.join(output_dir, output_filename)

        try:
            # Convert the PDF to a Docling document
            conv_result: ConversionResult = converter.convert(input_path)

            # Export the document to Markdown
            markdown_content = conv_result.document.export_to_markdown()

            # Save the Markdown content to a file
            with open(output_path, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_content)

            print(f"Successfully converted '{filename}' to '{output_filename}'")
        except Exception as e:
            print(f"Failed to convert '{filename}': {e}")
