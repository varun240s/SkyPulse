import pandas as pd
from datetime import datetime, timedelta

# Function to convert decimal year to date
def decimal_year_to_date(decimal_year):
    year = int(decimal_year)
    remainder = decimal_year - year
    start = datetime(year, 1, 1)
    days = (start.replace(year=year + 1) - start).days * remainder
    date = start + timedelta(days=days)
    return date.strftime("%Y-%m-%d")

# Define input and output file paths
input_file = r"E:\College Hackathon\CLIMATE CHANGE ANALYSIS\data\raw\co2_emissions.csv"
output_file = r"E:\College Hackathon\CLIMATE CHANGE ANALYSIS\data\formatted\co2_reformatted.csv"

# Load the dataset
df = pd.read_csv(input_file)

# Convert decimal date to YYYY-MM-DD
df["Date"] = df["decimal date"].apply(decimal_year_to_date)

# Extract relevant columns and rename
result = df[["Date", "average"]].rename(columns={"average": "CO2"})

# Save the cleaned data to CSV
result.to_csv(output_file, index=False)

print(f"Data successfully reformatted and saved to {output_file}")
