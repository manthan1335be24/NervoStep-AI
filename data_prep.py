import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

def create_sliding_windows(data_df, target_column, window_size=3000, step_size=1500):
    """
    Slices continuous sensor data into overlapping windows for ML input.
    
    Parameters:
    - data_df: Pandas DataFrame containing the sensor readings.
    - target_column: The name of the column containing the label (e.g., 'Walking_State').
    - window_size: Number of timesteps in a window (e.g., 3000 for 1 minute at 50Hz).
    - step_size: How far to slide the window forward (e.g., 1500 for a 50% overlap).
    
    Returns:
    - X: 3D numpy array of shape (num_windows, window_size, num_features)
    - y: 1D numpy array of labels corresponding to each window
    """
    
    # Separate features and labels
    features = data_df.drop(columns=[target_column]).values
    labels = data_df[target_column].values
    
    # Scale the features (Neural networks need standardized data)
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    X_windows = []
    y_windows = []
    
    # Slide through the data
    for i in range(0, len(features_scaled) - window_size, step_size):
        # Extract the 1-minute chunk
        window_chunk = features_scaled[i : i + window_size]
        
        # Get the most frequent label in this window
        window_label = np.bincount(labels[i : i + window_size]).argmax()
        
        X_windows.append(window_chunk)
        y_windows.append(window_label)
        
    return np.array(X_windows), np.array(y_windows)

# Example usage (commented out until we have real data):
# sample_data = pd.read_csv('../data/raw/physionet_autonomic/sample.csv')
# X_train, y_train = create_sliding_windows(sample_data, target_column='label')
# print(f"Prepared Data Shape: {X_train.shape}")