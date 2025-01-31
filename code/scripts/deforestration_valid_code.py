import pandas as pd
import os

# Load the deforestation JSON file into a DataFrame
file_path = "e:/College Hackathon/CLIMATE CHANGE ANALYSIS/data/formatted/deforestation.json"

# Check if the file exists
if not os.path.exists(file_path):
    print(f"Error: The file deforestation.json does not exist at the path {file_path}")
else:
    df = pd.read_json(file_path)

    # Extract unique region codes (valid codes) and convert them to a list
    valid_codes = df["Region"].unique().tolist()

    # Print the valid region codes as a list
    print("Valid region codes:", valid_codes)
