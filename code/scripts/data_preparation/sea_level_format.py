import pandas as pd

# Define input and output file paths
input_file = r"E:\College Hackathon\CLIMATE CHANGE ANALYSIS\data\raw\sea_level_data.csv"
output_file = r"E:\College Hackathon\CLIMATE CHANGE ANALYSIS\data\formatted\reformatted_sea_level.csv"

# Load the dataset
df = pd.read_csv(input_file)

# Clean the Date column (remove "D" and reformat)
df["Date"] = df["Date"].str.replace("D", "", regex=False)
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y").dt.strftime("%Y-%m-%d")

# Select and rename columns
result = df[["Date", "Value"]].rename(columns={"Value": "Sea Level"})

# Save the cleaned data to CSV
result.to_csv(output_file, index=False)

print(f"Data successfully reformatted and saved to {output_file}")
