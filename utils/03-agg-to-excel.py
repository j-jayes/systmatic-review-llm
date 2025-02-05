import pandas as pd
import json
from pathlib import Path

# Define directories
input_dir = Path("data/openai_output")
output_dir = Path("data/excel_output")
output_dir.mkdir(parents=True, exist_ok=True)

# Initialize a list to store all flattened data
all_data = []

# Function to flatten JSON data
def flatten_json(data, filename):
    metadata = data.get("metadata", {})
    relevance = data.get("relevance", {})
    design = data.get("design", {})
    key_variables = data.get("key_variables", {})
    dependent_variables = key_variables.get("dependent_variables", {})
    qualitative_data = data.get("qualitative_data") or {}
    historical_context = data.get("historical_context", {})
    outcomes = data.get("outcomes", {})
    quality_assessment = data.get("quality_assessment", {})

    return {
        "filename": filename,
        "authors": ", ".join(metadata.get("authors", [])),
        "title": metadata.get("title", ""),
        "year_of_publication": metadata.get("year_of_publication", ""),
        "journal_or_publisher": metadata.get("journal_or_publisher", ""),
        "topic": relevance.get("topic", ""),
        "relevance": relevance.get("relevance", ""),
        "technologies": ", ".join(relevance.get("technologies", [])),
        "study_type": design.get("study_type", ""),
        "methodology": design.get("methodology", ""),
        "occupations": ", ".join(design.get("occupations", [])),
        "occupation_types": ", ".join(design.get("occupation_types", [])),
        "gross_vs_net": design.get("gross_vs_net", ""),
        "time_period_covered": design.get("time_period_covered", ""),
        "time_period_start": design.get("time_period_start", ""),
        "time_period_end": design.get("time_period_end", ""),
        "geographical_focus": design.get("geographical_focus", ""),
        "independent_variables": ", ".join(key_variables.get("independent_variables", [])),
        "displaced": dependent_variables.get("displaced", ""),
        "unemployment_or_underemployment": dependent_variables.get("unemployment_or_underemployment", ""),
        "key_themes": ", ".join(qualitative_data.get("key_themes", [])),
        "narrative_descriptions": qualitative_data.get("narrative_descriptions", ""),
        "technological_changes": ", ".join(historical_context.get("technological_changes", [])),
        "economic_conditions": historical_context.get("economic_conditions", ""),
        "institutional_context": historical_context.get("institutional_context", ""),
        "main_findings": outcomes.get("main_findings", ""),
        "conclusions": outcomes.get("conclusions", ""),
        "long_term_impacts": outcomes.get("long_term_impacts", ""),
        "methodological_limitations": quality_assessment.get("methodological_limitations", ""),
        "coherence": quality_assessment.get("coherence", ""),
        "adequacy_of_data": quality_assessment.get("adequacy_of_data", ""),
        "relevance_quality": quality_assessment.get("relevance", ""),
        "overall_confidence": quality_assessment.get("overall_confidence", ""),
        "inclusion_decision": quality_assessment.get("inclusion_decision", "")
    }

# Process all JSON files in the input directory
for json_file in input_dir.glob("*.json"):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            flattened_data = flatten_json(data, json_file.name)
            all_data.append(flattened_data)
    except (json.JSONDecodeError, TypeError, AttributeError) as e:
        print(f"Error processing file {json_file}: {e}")

# Convert the collected data into a DataFrame
df = pd.DataFrame(all_data)

# Save the DataFrame to an Excel file
output_file = output_dir / "labor_displacement_studies.xlsx"
df.to_excel(output_file, index=False)

print(f"Excel file saved to {output_file}")
