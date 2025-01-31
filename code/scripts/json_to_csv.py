import os
import csv
import json

def convert_csv_to_json(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [row for row in csv_reader]
    
    with open(output_file, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2)
    
    print(f"Converted: {input_file} -> {output_file}")

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for file in os.listdir(input_dir):
        full_path = os.path.join(input_dir, file)
        output_file_path = os.path.join(output_dir, file.replace('.csv', '.json'))
        
        if os.path.isfile(full_path) and file.endswith('.csv'):
            convert_csv_to_json(full_path, output_file_path)

input_dirs = [
    r"E:\\College Hackathon\\CLIMATE CHANGE ANALYSIS\\frontend\\public\\data\\predictions",
    r"E:\\College Hackathon\\CLIMATE CHANGE ANALYSIS\\frontend\\public\\data\\processed"
]
output_dir = r"E:\\College Hackathon\\CLIMATE CHANGE ANALYSIS\\frontend\\public\\data\\json"

for input_dir in input_dirs:
    process_directory(input_dir, output_dir)