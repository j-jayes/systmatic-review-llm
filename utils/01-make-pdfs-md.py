import os
import signal
import fitz  # PyMuPDF
from docling.document_converter import DocumentConverter
from docling.datamodel.document import ConversionResult
import pymupdf4llm


# Initialize the DocumentConverter
converter = DocumentConverter()

# Define input and output directories
input_dir = 'data/pdfs/'
output_dir = 'data/markdown/'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define a handler for the timeout
def handler(signum, frame):
    raise TimeoutError("Conversion timed out")

# Set the signal handler for SIGALRM
signal.signal(signal.SIGALRM, handler)

# Function to convert PDF to markdown using PyMuPDF as a fallback
def convert_with_pymupdf(input_path, output_path):
    try:
        # Convert the PDF to Markdown using pymupdf4llm
        markdown_content = pymupdf4llm.to_markdown(input_path)

        # Save the Markdown content to a file
        with open(output_path, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown_content)

        print(f"Fallback conversion of '{os.path.basename(input_path)}' using pymupdf4llm succeeded.")
    except Exception as e:
        print(f"Fallback conversion of '{os.path.basename(input_path)}' failed: {e}")

# Iterate over all files in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith('.pdf'):
        input_path = os.path.join(input_dir, filename)
        output_filename = f"{os.path.splitext(filename)[0]}.md"
        output_path = os.path.join(output_dir, output_filename)

        # Check if the .md file already exists
        if os.path.exists(output_path):
            print(f"'{output_filename}' already exists. Skipping conversion.")
            continue

        try:
            # Set an alarm for 5 minutes (300 seconds)
            signal.alarm(10)

            # Convert the PDF to a Docling document
            conv_result: ConversionResult = converter.convert(input_path)

            # Export the document to Markdown
            markdown_content = conv_result.document.export_to_markdown()

            # Save the Markdown content to a file
            with open(output_path, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_content)

            print(f"Successfully converted '{filename}' to '{output_filename}'")
        
        except TimeoutError:
            print(f"Conversion of '{filename}' timed out. Using PyMuPDF as fallback.")
            convert_with_pymupdf(input_path, output_path)
        
        except Exception as e:
            print(f"Failed to convert '{filename}' using Docling: {e}. Attempting fallback with PyMuPDF.")
            convert_with_pymupdf(input_path, output_path)

        finally:
            # Cancel the alarm
            signal.alarm(0)
