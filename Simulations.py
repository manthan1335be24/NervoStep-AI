import pandas as pd

def generate_telemetry_simulation(periods=10):
    """
    Generates simulated longitudinal temperature and risk telemetry data.
    
    Args:
        periods (int): The number of days of data to generate.
        
    Returns:
        pd.DataFrame: A DataFrame containing simulated 'Date', 'Heel Temp', 
                      'Toe Temp', and 'Risk Level' data.
    """
    # Generate dates up to today
    dates = pd.date_range(end=pd.Timestamp.today(), periods=periods, freq='D')
    
    # Static simulated data arrays (matching the original code)
    # Note: If periods > 10, these static arrays would need to be expanded 
    # or generated dynamically.
    heel_temps = [32, 32.2, 31.8, 32.5, 33, 32.8, 32.1, 32.4, 32.6, 33.1]
    toe_temps = [34, 34.5, 34.2, 34.8, 34.1, 34.3, 34.6, 34.4, 34.7, 34.9]
    risk_levels = [1, 1, 1, 0, 0, 1, 0, 0, 1, 0]
    
    # Create the DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Heel Temp': heel_temps[:periods], # Slice in case periods < 10
        'Toe Temp': toe_temps[:periods],
        'Risk Level': risk_levels[:periods]
    })
    
    return df

# Example usage:
if __name__ == "__main__":
    simulated_data = generate_telemetry_simulation()
    print(simulated_data)