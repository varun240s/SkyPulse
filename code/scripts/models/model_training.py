import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
import os
from datetime import datetime

# Configure paths
CLEANED_PATH = r'E:\College Hackathon\CLIMATE CHANGE ANALYSIS\data\cleaned'
PREDICTIONS_PATH = r'E:\College Hackathon\CLIMATE CHANGE ANALYSIS\data\predictions'

# Ensure the processed directory exists
os.makedirs(CLEANED_PATH, exist_ok=True)

def load_and_prepare_data():
    """Load and prepare all datasets with proper date handling"""
    # Load cleaned datasets
    temperature = pd.read_csv(os.path.join(CLEANED_PATH, 'cleaned_temperature.csv'), parse_dates=['Date'])
    co2 = pd.read_csv(os.path.join(CLEANED_PATH, 'cleaned_co2.csv'), parse_dates=['Date'])
    deforestation = pd.read_csv(os.path.join(CLEANED_PATH, 'cleaned_deforestation.csv'))
    
    # Convert deforestation Year to Date (assuming year-end)
    deforestation['Date'] = pd.to_datetime(deforestation['Year'].astype(str) + '-12-31')
    deforestation.drop('Year', axis=1, inplace=True)
    
    return temperature, co2, deforestation

def arima_forecast(series, forecast_years=30):
    """ARIMA forecasting with proper frequency handling"""
    try:
        # Set explicit frequency
        series = series.asfreq('D').ffill()
        
        # Fit ARIMA model
        model = ARIMA(series, order=(2, 1, 2))
        results = model.fit()
        
        # Forecast future values
        forecast = results.get_forecast(steps=forecast_years*365)  # Daily steps for 30 years
        forecast_df = pd.DataFrame({
            'Date': pd.date_range(start=series.index[-1], periods=forecast_years*365 + 1, freq='D')[1:],
            'Predicted': forecast.predicted_mean
        })
        
        # Resample to annual
        forecast_df = forecast_df.resample('YE', on='Date').mean().reset_index()
        return forecast_df
    except Exception as e:
        print(f"ARIMA error: {str(e)}")
        return None

def prophet_forecast(df, date_col, value_col, forecast_years=30):
    """Prophet forecasting with updated frequency"""
    try:
        # Prepare data for Prophet
        prophet_df = df[[date_col, value_col]].copy()
        prophet_df.columns = ['ds', 'y']
        
        # Fit Prophet model
        model = Prophet()
        model.fit(prophet_df)
        
        # Make future predictions with correct frequency
        future = model.make_future_dataframe(periods=forecast_years, freq='YE')
        forecast = model.predict(future)
        
        # Format output
        forecast_df = forecast[['ds', 'yhat']].rename(columns={'ds': 'Date', 'yhat': 'Predicted'})
        return forecast_df
    except Exception as e:
        print(f"Prophet error: {str(e)}")
        return None

def random_forest_regression(temp_df, co2_df, deforestation_df):
    """Random Forest with proper date merging"""
    try:
        # Merge datasets on Date
        merged = temp_df.merge(co2_df, on='Date', how='inner')
        merged = merged.merge(deforestation_df, on='Date', how='left')
        
        # Handle missing values
        merged['Area_Deforested'].fillna(0, inplace=True)
        
        # Create temporal features
        merged['Year'] = merged['Date'].dt.year
        merged['Month'] = merged['Date'].dt.month
        
        # Split data
        train = merged[merged['Year'] < 2000]
        test = merged[merged['Year'] >= 2000]
        
        if train.empty or test.empty:
            raise ValueError("Insufficient data for train/test split")
            
        # Prepare features
        features = ['CO2', 'Area_Deforested', 'Year', 'Month']
        X_train = train[features]
        y_train = train['Temperature']
        X_test = test[features]
        y_test = test['Temperature']
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Evaluate
        metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred),
            'mae': mean_absolute_error(y_test, y_pred)
        }
        
        # Format output
        predictions = pd.DataFrame({
            'Date': test['Date'],
            'Actual': y_test,
            'Predicted': y_pred
        })
        return predictions, metrics
    except Exception as e:
        print(f"Random Forest error: {str(e)}")
        return None, None

if __name__ == "__main__":
    # Load and prepare data
    temperature, co2, deforestation = load_and_prepare_data()
    
    # Time-Series Forecasting
    print("Running ARIMA for temperature forecasting...")
    temp_series = temperature.set_index('Date')['Temperature']
    arima_predictions = arima_forecast(temp_series)
    if arima_predictions is not None:
        arima_predictions.to_csv(os.path.join(PREDICTIONS_PATH, 'arima_temperature_predictions.csv'), index=False)
    
    print("\nRunning Prophet for CO2 forecasting...")
    prophet_predictions = prophet_forecast(co2, 'Date', 'CO2')
    if prophet_predictions is not None:
        prophet_predictions.to_csv(os.path.join(PREDICTIONS_PATH, 'prophet_co2_predictions.csv'), index=False)
    
    # Random Forest Regression
    print("\nRunning Random Forest for multi-variable impact...")
    rf_predictions, rf_metrics = random_forest_regression(temperature, co2, deforestation)
    if rf_predictions is not None:
        rf_predictions.to_csv(os.path.join(PREDICTIONS_PATH, 'random_forest_predictions.csv'), index=False)
        print(f"\nRandom Forest Metrics:")
        print(f"MSE: {rf_metrics['mse']:.2f}")
        print(f"R²: {rf_metrics['r2']:.2f}")
        print(f"MAE: {rf_metrics['mae']:.2f}")
    
    print("\nPredictive modeling complete! Check output files.")