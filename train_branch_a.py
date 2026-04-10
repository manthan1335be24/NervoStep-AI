import wfdb
import os
import numpy as np
import pandas as pd
import neurokit2 as nk
import tensorflow as tf
from tensorflow.keras import layers, models, regularizers
from sklearn.model_selection import GroupShuffleSplit
from sklearn.utils import class_weight

def load_physionet_with_labels():
    print("🩺 Processing ECG Vitals with Subject-Aware Splitting...")
    base_dir = 'data/raw/physionet_autonomic/'
    info_path = os.path.join(base_dir, 'subject-info.csv')
    
    df_info = pd.read_csv(info_path)
    df_info['ID'] = df_info['ID'].astype(str).str.zfill(4) 
    
    all_vitals, all_labels, groups = [], [], []
    record_ids = df_info['ID'].values[:400] 

    for rid in record_ids:
        try:
            record_path = os.path.join(base_dir, rid)
            if not os.path.exists(record_path + '.hea'): continue
            
            signals, fields = wfdb.rdsamp(record_path)
            fs = fields['fs']
            ecg_col = [i for i, s in enumerate(fields['sig_name']) if 'ECG' in s][0]
            ecg_data = signals[:, ecg_col]
            
            chunk_size = 60 * fs
            if len(ecg_data) >= chunk_size:
                ecg_chunk = ecg_data[:chunk_size]
                signals_nk, _ = nk.ecg_process(ecg_chunk, sampling_rate=fs)
                bpm = signals_nk['ECG_Rate'].values
                
                # Normalization: Scale 60-100 BPM to 0.0-1.0
                bpm_norm = (bpm[::fs] - 60) / (100 - 60) 
                bpm_norm = np.clip(bpm_norm, 0, 1)
                
                age_group = df_info[df_info['ID'] == rid]['Age_group'].values[0]
                if age_group <= 3:
                    all_vitals.append(bpm_norm.reshape(-1, 1))
                    all_labels.append(0)
                    groups.append(rid) # Track Subject ID
                elif age_group >= 8:
                    all_vitals.append(bpm_norm.reshape(-1, 1))
                    all_labels.append(1)
                    groups.append(rid)
        except Exception: continue 

    return np.array(all_vitals), np.array(all_labels), np.array(groups)

def build_branch_a_model(input_shape):
    model = models.Sequential([
        layers.Input(shape=input_shape),
        layers.GaussianNoise(0.02), # Prevents memorization of signal noise
        layers.GRU(32, return_sequences=True, kernel_regularizer=regularizers.l2(0.01)),
        layers.BatchNormalization(),
        layers.Dropout(0.5), # Higher dropout to fight overfitting
        layers.GRU(16),
        layers.Dense(16, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

if __name__ == "__main__":
    X, y, groups = load_physionet_with_labels()
    
    # Subject-Based Split: 80% of PEOPLE for training, 20% for testing
    gss = GroupShuffleSplit(n_splits=1, train_size=0.8, random_state=42)
    train_idx, test_idx = next(gss.split(X, y, groups))
    
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    
    weights = class_weight.compute_class_weight('balanced', classes=np.unique(y), y=y)
    model = build_branch_a_model(input_shape=(60, 1))
    model.fit(X_train, y_train, epochs=30, batch_size=16, 
              validation_data=(X_test, y_test), class_weight=dict(enumerate(weights)))
    
    os.makedirs('models/pretrained', exist_ok=True)
    model.save('models/pretrained/branch_a_vitals.h5')