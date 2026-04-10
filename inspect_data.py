import numpy as np
import os

def inspect_file():
    # Pick exactly one file that we know exists from your logs
    file_path = os.path.join('data', 'raw', 'ieee_plantar', 'RBNew', '000.npy')
    
    print(f"--- X-Raying File: {file_path} ---")
    
    try:
        # Load the file
        data = np.load(file_path, allow_pickle=True)
        
        print(f"1. Main Data Type: {type(data)}")
        print(f"2. Main Data Shape: {data.shape}")
        
        # If it's a hidden dictionary
        if data.ndim == 0:
            print("3. Structure: 0-D Array (Hidden Dictionary/Object detected)")
            hidden_data = data.item()
            print(f"4. Hidden Type: {type(hidden_data)}")
            
            if isinstance(hidden_data, dict):
                print("\n--- Dictionary Keys Found ---")
                for key, val in hidden_data.items():
                    print(f"Key: '{key}' | Type: {type(val)}")
                    if isinstance(val, np.ndarray):
                        print(f"   -> Array Shape: {val.shape}")
            
        else:
            print("3. Structure: Standard Array")
            print(f"4. Preview of first item shape: {np.array(data[0]).shape}")
            print(f"5. Preview of first item type: {type(data[0])}")

    except Exception as e:
        print(f"Error during inspection: {e}")

if __name__ == "__main__":
    inspect_file()