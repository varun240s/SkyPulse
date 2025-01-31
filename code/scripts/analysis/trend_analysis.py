import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import os

# Get absolute path to project root
project_root = r'E:\College Hackathon\CLIMATE CHANGE ANALYSIS'
cleaned_path = os.path.join(project_root, 'data', 'cleaned')
processed_path = os.path.join(project_root, 'data', 'processed')

# Create directories if they don't exist
os.makedirs(cleaned_path, exist_ok=True)

# Load cleaned datasets with absolute paths
def load_data():
    return {
        'temperature': pd.read_csv(os.path.join(cleaned_path, 'cleaned_temperature.csv'), parse_dates=['Date']),
        'co2': pd.read_csv(os.path.join(cleaned_path, 'cleaned_co2.csv'), parse_dates=['Date']),
        'sea_level': pd.read_csv(os.path.join(cleaned_path, 'cleaned_sea_level.csv'), parse_dates=['Date']),
        'deforestation': pd.read_csv(os.path.join(cleaned_path, 'cleaned_deforestation.csv'))
    }

def analyze_temperature(temp_df):
    try:
        # Time series decomposition
        temp_series = temp_df.set_index('Date')['Temperature']
        decomposition = seasonal_decompose(temp_series.resample('YE').mean(), model='additive', period=10)
        
        # Calculate decadal trends
        temp_df['Decade'] = (temp_df['Date'].dt.year // 10) * 10
        decadal_avg = temp_df.groupby('Decade')['Temperature'].mean().reset_index()
        
        # Save results
        decomposition.plot().savefig(os.path.join(processed_path, 'temp_decomposition.png'))
        decadal_avg.to_csv(os.path.join(processed_path, 'decadal_temperature.csv'), index=False)
        
        return decadal_avg
    except Exception as e:
        print(f"Error in temperature analysis: {str(e)}")
        return None

def analyze_co2(co2_df):
    try:
        # Calculate annual average
        co2_annual = co2_df.resample('YE', on='Date').mean().reset_index()
        
        # Linear trend calculation
        co2_annual['Year'] = co2_annual['Date'].dt.year
        slope, intercept, _, _, _ = stats.linregress(co2_annual['Year'], co2_annual['CO2'])
        
        # Save results
        co2_annual.to_csv(os.path.join(processed_path, 'annual_co2.csv'), index=False)
        return slope, intercept
    except Exception as e:
        print(f"Error in CO2 analysis: {str(e)}")
        return None, None

def calculate_correlations(temp_df, co2_df, sea_df):
    try:
        # Prepare dataframes
        temp_annual = temp_df.resample('YE', on='Date').mean().reset_index()
        co2_annual = co2_df.resample('YE', on='Date').mean().reset_index()
        sea_level_annual = sea_df.resample('YE', on='Date').mean().reset_index()
        
        # Merge datasets
        merged = temp_annual.merge(co2_annual, on='Date').merge(sea_level_annual, on='Date')
        
        # Calculate correlation matrix
        corr_matrix = merged[['Temperature', 'CO2', 'Sea Level']].corr()
        
        # Save results
        corr_matrix.to_csv(os.path.join(processed_path, 'correlation_matrix.csv'))
        return corr_matrix
    except Exception as e:
        print(f"Error in correlation calculation: {str(e)}")
        return None

def co2_temp_regression(temp_df, co2_df):
    try:
        # Merge CO2 and Temperature data
        merged = temp_df.merge(co2_df, on='Date', how='inner')
        
        # Calculate linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            merged['CO2'], merged['Temperature']
        )
        
        # Create trend line
        merged['Predicted'] = slope * merged['CO2'] + intercept
        
        # Save results
        merged.to_csv(os.path.join(processed_path, 'co2_temp_regression.csv'), index=False)
        return {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_value**2,
            'p_value': p_value,
            'std_err': std_err
        }
    except Exception as e:
        print(f"Error in regression analysis: {str(e)}")
        return None

if __name__ == "__main__":
    data = load_data()
    
    print("Analyzing temperature trends...")
    temp_results = analyze_temperature(data['temperature'])
    
    print("\nAnalyzing CO2 trends...")
    co2_slope, co2_intercept = analyze_co2(data['co2'])
    
    print("\nCalculating correlations...")
    correlations = calculate_correlations(data['temperature'], data['co2'], data['sea_level'])
    
    print("\nRunning CO2-Temperature regression...")
    regression_results = co2_temp_regression(data['temperature'], data['co2'])
    
    if all([temp_results is not None, co2_slope is not None, correlations is not None, regression_results is not None]):
        print("\nAnalysis complete!")
        print(f"CO2 annual increase rate: {co2_slope:.2f} ppm/year")
        print(f"CO2-Temperature R-squared: {regression_results['r_squared']:.3f}")
        print(f"Files saved to: {processed_path}")
    else:
        print("\nAnalysis completed with some errors. Check output files.")