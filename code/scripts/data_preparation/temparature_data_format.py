import pandas as pd

# Define input and output file paths
input_file = r"E:\College Hackathon\CLIMATE CHANGE ANALYSIS\data\raw\temperature.csv"
output_file = r"E:\College Hackathon\CLIMATE CHANGE ANALYSIS\data\formatted\temperature_formatted.csv"

# Load the data, skipping the header description
df = pd.read_csv(input_file, skiprows=1)

# Melt the dataframe to convert months into rows
melted = df.melt(
    id_vars=["Year"],
    value_vars=["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    var_name="Month",
    value_name="Temperature"
)

# Map month abbreviations to numbers (e.g., "Jan" → 1)
month_to_num = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}
melted["Month"] = melted["Month"].map(month_to_num)

# Drop rows with missing Year/Month and convert to integers
melted = melted.dropna(subset=["Year", "Month"])

# Debugging: Check for non-integer values in Year and Month
print("Unique Year values before conversion:", melted["Year"].unique())
print("Unique Month values before conversion:", melted["Month"].unique())

# Convert Year and Month to integers
melted["Year"] = melted["Year"].astype(int)
melted["Month"] = melted["Month"].astype(int)

# Debugging: Verify conversion
print("Unique Year values after conversion:", melted["Year"].unique())
print("Unique Month values after conversion:", melted["Month"].unique())

# Generate daily dates for each month using pandas
def generate_dates(row):
    try:
        start_date = pd.Timestamp(year=int(row["Year"]), month=int(row["Month"]), day=1)
        end_date = start_date + pd.offsets.MonthEnd(1)
        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        return dates.strftime("%Y-%m-%d").tolist()
    except Exception as e:
        print(f"Error generating dates for row: {row}. Error: {e}")
        return []

melted["Date"] = melted.apply(generate_dates, axis=1)

# Explode the dates into rows and finalize
exploded = melted.explode("Date")
result = exploded[["Date", "Temperature"]].sort_values("Date").reset_index(drop=True)

# Save to CSV
result.to_csv(output_file, index=False)

print(f"Data successfully reformatted and saved to {output_file}")