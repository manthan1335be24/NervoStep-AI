import numpy as np
import os

def check_step_size():
    file_path = os.path.join('data', 'raw', 'ieee_plantar', 'RBNew', '000.npy')
    data = np.load(file_path, allow_pickle=True).item()
    
    left = np.array(data.get('LeftFrame', []))
    right = np.array(data.get('RightFrame', []))
    
    print(f"Left Foot Shape: {left.shape}")
    print(f"Right Foot Shape: {right.shape}")

if __name__ == "__main__":
    check_step_size()