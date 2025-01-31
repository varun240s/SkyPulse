import os
import pandas as pd
import numpy as np
from scipy.stats import zscore

# Define paths
# PROCESSED_DATA_PATH = "e:/College Hackathon/CLIMATE CHANGE ANALYSIS/data/processed/"
CLEANED_DATA_PATH = "e:/College Hackathon/CLIMATE CHANGE ANALYSIS/data/cleaned/"
os.makedirs(CLEANED_DATA_PATH, exist_ok=True)

def clean_co2_data(file_path):
    """Clean CO2 dataset with enhanced outlier detection and date handling"""
    try:
        df = pd.read_csv(file_path, parse_dates=['Date'])
        
        # Set 'Date' column as the index
        df.set_index('Date', inplace=True)
        
        # Handle missing values with time-based interpolation
        df['CO2'] = df['CO2'].interpolate(method='time')
        
        # Remove physically impossible values (modern CO2 range: 300-5000 ppm)
        df = df[(df['CO2'] > 250) & (df['CO2'] < 5000)]
        
        # Save cleaned data
        df.to_csv(os.path.join(CLEANED_DATA_PATH, "cleaned_co2.csv"))
        print("CO2 data cleaned successfully. Records:", len(df))
        
    except Exception as e:
        print(f"Error cleaning CO2 data: {str(e)}")

def clean_deforestation_data(file_path):
    """Clean deforestation data with regional validation and improved outlier handling"""
    try:
        df = pd.read_json(file_path)
        
        # Validate regions (example using ISO3 country codes)
        valid_regions = ['AGO', 'ARG', 'AUS', 'BDI', 'BES', 'BGD', 'BHS', 'BLZ', 'BOL', 'BRA', 'BRN'
                         , 'BTN', 'CAF', 'CHN', 'CIV', 'CMR', 'COD', 'COG', 'COL', 'CRI', 'CUB', 'CYM',
                         'DMA', 'DOM', 'ECU', 'ETH', 'FJI', 'GAB', 'GHA', 'GIN', 'GLP', 'GNB', 'GNQ', 'GTM',
                         'GUF', 'GUY', 'HND', 'HTI', 'IDN', 'IND', 'JAM', 'KEN', 'KHM', 'KNA', 'LAO', 'LBR',
                         'LCA', 'LKA', 'MAF', 'MDG', 'MDV', 'MEX', 'MMR', 'MOZ', 'MSR', 'MTQ', 'MWI', 'MYS',
                         'NGA', 'NIC', 'NPL', 'PAN', 'PER', 'PHL', 'PLW', 'PNG', 'PRI', 'PRY', 'RWA', 'SLB',
                         'SLE', 'SLV', 'SSD', 'SUR', 'SXM', 'TCA', 'TGO', 'THA', 'TTO', 'TWN', 'TZA', 'UGA',
                         'USA', 'VCT', 'VEN', 'VGB', 'VIR', 'VNM', 'VUT', 'ZAF', 'ZMB', 'ZWE', 'BEN', 'SEN',
                         'SGP', 'UMI', 'ABW', 'ATG', 'GMB']  # Add all valid codes
                         
        df = df[df['Region'].isin(valid_regions)]
        
        # Remove negative deforestation values
        df = df[df['Area_Deforested'] >= 0]
        
        # Handle outliers using IQR (more robust for skewed data)
        Q1 = df['Area_Deforested'].quantile(0.25)
        Q3 = df['Area_Deforested'].quantile(0.75)
        IQR = Q3 - Q1
        df = df[~((df['Area_Deforested'] < (Q1 - 1.5 * IQR)) | 
                 (df['Area_Deforested'] > (Q3 + 1.5 * IQR)))]

        # Save cleaned data
        df.to_csv(os.path.join(CLEANED_DATA_PATH, "cleaned_deforestation.csv"), index=False)
        print("Deforestation data cleaned successfully. Records:", len(df))
        
    except Exception as e:
        print(f"Error cleaning deforestation data: {str(e)}")

def clean_sea_level_data(file_path):
    """Clean sea level data with enhanced missing value handling"""
    try:
        df = pd.read_csv(file_path, parse_dates=['Date'])
        
        # Set 'Date' column as the index
        df.set_index('Date', inplace=True)
        
        # Convert empty strings to NaN and interpolate
        df['Sea Level'] = pd.to_numeric(df['Sea Level'], errors='coerce')
        df['Sea Level'] = df['Sea Level'].interpolate(method='time')
        
        # Remove extreme outliers (±3σ from rolling 30-day mean)
        rolling_mean = df['Sea Level'].rolling(window=30, min_periods=1).mean()
        rolling_std = df['Sea Level'].rolling(window=30, min_periods=1).std()
        df = df[abs(df['Sea Level'] - rolling_mean) < 3 * rolling_std]
        
        # Save cleaned data
        df.to_csv(os.path.join(CLEANED_DATA_PATH, "cleaned_sea_level.csv"))
        print("Sea level data cleaned successfully. Records:", len(df))
        
    except Exception as e:
        print(f"Error cleaning sea level data: {str(e)}")

def clean_temperature_data(file_path):
    """Clean temperature data with improved date handling and validation"""
    try:
        df = pd.read_csv(file_path, parse_dates=['Date'])
        
        # Set 'Date' column as the index
        df.set_index('Date', inplace=True)
        
        # Handle missing values with time-based interpolation
        df['Temperature'] = df['Temperature'].interpolate(method='time')
        
        # Remove physically impossible values (global temperature anomaly range)
        df = df[(df['Temperature'] > -5) & (df['Temperature'] < 5)]
        
        # Save cleaned data
        df.to_csv(os.path.join(CLEANED_DATA_PATH, "cleaned_temperature.csv"))
        print("Temperature data cleaned successfully. Records:", len(df))
        
    except Exception as e:
        print(f"Error cleaning temperature data: {str(e)}")

if __name__ == "__main__":
    # Input paths
    DATA_PATH = "e:/College Hackathon/CLIMATE CHANGE ANALYSIS/data/formatted/"
    
    # Clean all datasets
    clean_co2_data(os.path.join(DATA_PATH, "co2_reformatted.csv"))
    clean_deforestation_data(os.path.join(DATA_PATH, "deforestation.json"))
    clean_sea_level_data(os.path.join(DATA_PATH, "sea_level_data_formatted.csv"))
    clean_temperature_data(os.path.join(DATA_PATH, "temperature_formatted.csv"))
