import os
import json
from openai import OpenAI, OpenAIError, BadRequestError, APIError
import logging
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set your OpenAI API key; ensure it's stored in your environment.
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

# Directory paths
MARKDOWN_DIR = "data/markdown"
OUTPUT_DIR = "data/openai_output"

# Create the output directory if it doesn't exist.
os.makedirs(OUTPUT_DIR, exist_ok=True)

class StudyMetadata(BaseModel):
    authors: List[str] = Field(..., description="Names of the study authors.")
    title: str = Field(..., description="Full title of the study.")
    year_of_publication: int = Field(..., description="The year in which the study was published.")
    journal_or_publisher: str = Field(..., description="Name of the journal or publication outlet.")

class StudyDesign(BaseModel):
    study_type: str = Field(..., description='e.g., "qualitative", "quantitative", "mixed-methods"')
    methodology: str = Field(..., description="The study's research method, e.g., historical analysis, econometric modeling, case study.")
    occupations: List[str] = Field(..., description="List of the occupation or occupations studied.")
    occupation_types: List[str] = Field(..., description='Specify whether the occupations are "Main", "Supplementary", or "Seasonal".')
    occupation_classifications: Optional[List[str]] = Field(None, description="Optional occupational coding of these occupational titles, e.g., HISCO, ISCO, PSTI.")
    gross_vs_net: str = Field(..., description='Focus on "gross", "net", or both number of workers displaced.')
    sample_size: Optional[int] = Field(None, description="Number of workers or entities involved in the study, if reported.")
    sample_characteristics: Optional[str] = Field(None, description="Details on the demographics or geographical focus of the sample.")
    time_period_covered: str = Field(..., description="The historical timeframe or period covered by the study.")
    geographical_focus: str = Field(..., description="The region, country, or location where the study was conducted.")

class DependentVariables(BaseModel):
    displaced: Optional[str] = Field(None, description="Description of the number or share of workers displaced.")
    unemployment_or_underemployment: Optional[str] = Field(None, description="Employment outcomes post-displacement, e.g., details on unemployment or underemployment.")
    duration: Optional[str] = Field(None, description="Duration of unemployment/underemployment following technological adoption.")
    wage_changes: Optional[str] = Field(None, description="Description of wage differences after displacement.")

class KeyVariables(BaseModel):
    independent_variables: List[str] = Field(..., description="List of technological changes examined, e.g., mechanization, automation.")
    dependent_variables: DependentVariables = Field(..., description="Employment-related outcomes studied.")
    moderators: Optional[List[str]] = Field(None, description="Factors that might influence the relationship between technology and employment, e.g., education level, industry type, union presence.")

class QuantitativeData(BaseModel):
    effect_sizes: Optional[List[float]] = Field(None, description="Reported effect sizes, e.g., Pearson’s r, Cohen’s d.")
    statistical_measures: Optional[Dict[str, float]] = Field(None, description="Statistical measures like means, standard deviations, p-values, etc.")

class QualitativeData(BaseModel):
    key_themes: Optional[List[str]] = Field(None, description="Major themes related to labor displacement due to technological change.")
    text_fragments: Optional[List[str]] = Field(None, description="Relevant quotes or text fragments from the study.")
    narrative_descriptions: Optional[str] = Field(None, description="Summary of qualitative accounts detailing the processes and impacts of labor displacement.")

class HistoricalContext(BaseModel):
    technological_changes: List[str] = Field(..., description="Specific technological advancements or changes examined in the study.")
    economic_conditions: str = Field(..., description="Broader economic conditions during the time period studied, e.g., period of growth, recession.")
    institutional_context: str = Field(..., description="Details on labor policies, labor relations, or regulatory factors that may have affected employment outcomes.")

class Outcomes(BaseModel):
    main_findings: str = Field(..., description="Summary of the study's main findings related to labor displacement.")
    conclusions: str = Field(..., description="Study's conclusions regarding the effects of technological changes on employment.")
    long_term_impacts: Optional[str] = Field(None, description="Discussions on the long-term effects of displacement on individuals, families, or communities.")

class StudyExtraction(BaseModel):
    metadata: StudyMetadata = Field(..., description="Basic metadata about the study.")
    design: StudyDesign = Field(..., description="Study design and methodological details.")
    key_variables: KeyVariables = Field(..., description="Key variables extracted from the study.")
    quantitative_data: Optional[QuantitativeData] = Field(None, description="Quantitative data if available.")
    qualitative_data: Optional[QualitativeData] = Field(None, description="Qualitative data if available.")
    historical_context: HistoricalContext = Field(..., description="Historical and contextual information of the study.")
    outcomes: Outcomes = Field(..., description="Outcomes and conclusions of the study.")

# Extraction instructions that are sent along with the markdown file.
EXTRACTION_INSTRUCTIONS = r"""
You are an expert in extracting structured information on historical labor displacement caused by technological change. Please use the provided Pydantic data model as the extraction py.

Below are the instructions:
0. Read the markdown document containing the study details.
1. Extract all relevant study metadata, design details, key variables (including independent and dependent variables), quantitative data (if any), qualitative data (if any), historical context, and outcomes/conclusions from the markdown document.
2. Ensure that the extracted information conforms exactly to the provided Pydantic data model.
3. If any field is not present in the markdown document, output a null (or equivalent) value for that field.
4. Return a single JSON object that validates against the Pydantic model.

"""

def process_markdown_file(filepath: str):
    """
    Reads a markdown file, sends it to the GPT-4 API along with instructions and the Pydantic model,
    and saves the API output as a JSON file in the output directory.
    """
    logging.info(f"Processing file: {filepath}")

    # Read the markdown file content.
    with open(filepath, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    prompt = EXTRACTION_INSTRUCTIONS

    try:
        # Call the GPT-4 API. Adjust model name as needed.
        response = client.beta.chat.completions.parse(
            model="gpt-4o",  # or "gpt-4o" if that's the correct identifier
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Here is the study in markdown format:\n\n{markdown_content}"}

                # {"role": "user", "content": [
                #     {type: "text", "content": "Here is the study in markdown format:"},
                #     {type: "markdown", "content": markdown_content}
                # ]}
            ],
            response_format=StudyExtraction,
            max_tokens=4096,
            temperature=0.0
        )

        # Extract the response content.
        extracted_json = response.choices[0].message.content

        # Optionally, you can load and re-dump the JSON to ensure proper formatting.
        extracted_data = json.loads(extracted_json)

        # Determine the output file name based on the input markdown filename.
        filename = os.path.splitext(os.path.basename(filepath))[0]
        output_filepath = os.path.join(OUTPUT_DIR, f"{filename}.json")

        # Save the output JSON.
        with open(output_filepath, "w", encoding="utf-8") as outfile:
            json.dump(extracted_data, outfile, indent=2)

        logging.info(f"Processed and saved extraction for {filepath} to {output_filepath}")

    except Exception as e:
        logging.error(f"Error processing {filepath}: {e}")

def main():
    # Loop through each Markdown file in the specified directory.
    for file in os.listdir(MARKDOWN_DIR):
        if file.endswith(".md"):
            filepath = os.path.join(MARKDOWN_DIR, file)
            filename = os.path.splitext(file)[0]
            output_filepath = os.path.join(OUTPUT_DIR, f"{filename}.json")
            
            # Check if the JSON file already exists
            if os.path.exists(output_filepath):
                logging.info(f"Output file {output_filepath} already exists. Skipping.")
                continue
            
            process_markdown_file(filepath)

if __name__ == "__main__":
    main()
