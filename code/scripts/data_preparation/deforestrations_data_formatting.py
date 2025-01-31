import csv
import json

# Define the input and output file paths
input_file = r'E:\College Hackathon\CLIMATE CHANGE ANALYSIS\data\raw\deforestation.csv'
output_file = r'E:\College Hackathon\CLIMATE CHANGE ANALYSIS\data\formatted\deforestation_data.json'

# Initialize an empty list to store the data
data = []

# Open and read the CSV file
with open(input_file, mode='r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Extract relevant fields and convert to desired format
        record = {
            'Year': int(row['umd_tree_cover_loss__year']),
            'Region': row['iso'],
            'Area_Deforested': float(row['umd_tree_cover_loss__ha'])
        }
        data.append(record)

# Write the data to a JSON file
with open(output_file, mode='w') as jsonfile:
    json.dump(data, jsonfile, indent=4)

print(f'Data has been successfully converted and saved to {output_file}.')
