import sys
import pandas as pd
import json

def convert_value(value):
    # Convert the value to float if possible, otherwise, return the original value
    try:
        return float(value)
    except (ValueError, TypeError):
        return value

def excel_to_custom_json(excel_file_path, json_output_path):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file_path, index_col=0)

    # Convert the DataFrame to a list of dictionaries with handling different data types
    genes_list = [{gene: convert_value(value) for gene, value in record.items()} for record in df.to_dict(orient='records')]

    # If there's only one record, remove the outer square brackets
    if len(genes_list) == 1:
        genes_list = genes_list[0]

    # Create the final JSON structure as a string
    result_json = json.dumps({"genes": genes_list}, indent=None)

    # Add backslashes before double quotes
    result_json = result_json.replace('"', '\\"')

    # Enclose the entire JSON string in double quotes
    result_json = f'"{result_json}",'

    # Save the JSON string to the specified output path
    with open(json_output_path, 'w') as json_file:
        json_file.write(result_json)

if __name__ == "__main__":
    # Check if the user provided both Excel file path and output JSON file path as command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <excel_file_path> <json_output_path>")
        sys.exit(1)

    # Get the Excel file path and output JSON file path from the command-line arguments
    excel_file_path = sys.argv[1]
    json_output_path = sys.argv[2]

    # Call the function to convert the Excel file to custom JSON as a string and save to a text file
    excel_to_custom_json(excel_file_path, json_output_path)

    print(f"Conversion completed. JSON string saved to {json_output_path}")
