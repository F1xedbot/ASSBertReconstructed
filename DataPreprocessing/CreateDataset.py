import os
import pandas as pd
import logging
from tqdm import tqdm
from ContractFormater import SourceCodeFormater
from ContractCleaner import SourceCodeCleaner

# Set up a logger
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Function to process source code and handle errors
def process_source_code_with_error_handling(input_file, output_file):
    try:
        cleaner = SourceCodeCleaner(input_file, output_file)
        cleaner.read_input_file()
        deleted_lines = cleaner.removal()
        formatter = SourceCodeFormater(cleaner.source_code, cleaner.parsed_source, deleted_lines)

        formatter.format_source(formatter.parsed_code)
        formatter.format_inheritance()

        cleaner = SourceCodeCleaner(source_code=formatter.source_code)
        cleaner.clean_source_code()
        return cleaner.source_code
    except Exception as e:
        error_message = f"Error processing file {input_file}: {str(e)}"
        logging.error(error_message)
        return None

# Function to clean and convert filename to integer
def clean_and_convert_filename(filename):
    # Remove non-numeric characters and convert to integer
    cleaned_filename = ''.join(filter(str.isdigit, filename))
    return int(cleaned_filename)

# Paths to your input and output directories
input_dir = 'ExperimentalDataset'
output_dir = 'ExperimentalParsedDataset'
excel_file = 'Labels/Excel Labels/merged_labels.xlsx'  # Change the file extension to .xlsx

# Load the labels from the merged_labels.xlsx Excel file
labels_df = pd.read_excel(excel_file, sheet_name='FullLabels')  # Replace 'your_sheet_name' with the correct sheet name

# Create a list to store the data as JSON objects
json_data = []

# Get a list of SOL files in the input directory
sol_files = [file for file in os.listdir(input_dir) if file.endswith('.sol')]

# Wrap the loop with tqdm to create a progress bar
for file in tqdm(sol_files, desc='Processing files'):
    # Construct the full path to the source code file
    source_code_file = os.path.join(input_dir, file)

    # Get the file name without extension and apply strip
    file_name = os.path.splitext(file)[0].strip()

    # Clean and convert the file_name to an integer
    file_name_integer = clean_and_convert_filename(file_name)

    # Check if the integer filename exists in labels_df
    if file_name_integer in labels_df['file'].values:
        # Look up the label for the file in labels_df
        label = labels_df.loc[labels_df['file'] == file_name_integer, 'label'].values[0]

         # Construct the full path to the output JSON file
        output_json_file = os.path.join(output_dir, file_name + '.json')

        # Process the source code with error handling
        processed_code = process_source_code_with_error_handling(source_code_file, output_json_file)

        if processed_code is not None:
            # Convert the label to a regular integer
            label = int(label)

            # Create a JSON object for the current file
            json_object = {
                'source_code': processed_code,
                'label': label
            }

            # Append the JSON object to the list
            json_data.append(json_object)

# Save the model data to ModelDataset.json
import json
with open('ModelDataset.json', 'w') as json_file:
    json.dump(json_data, json_file)
