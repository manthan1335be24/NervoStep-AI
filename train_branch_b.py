import os
import glob
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, regularizers
from sklearn.model_selection import train_test_split

def load_ieee_plantar_data():
    print("🚀 Loading Gait Data with Global Normalization...")
    base_dir = os.path.join('data', 'raw', 'ieee_plantar')
    class_mapping = {'NormalNew': 0, 'LBNew': 1, 'RBNew': 2}
    all_samples, all_labels = [], []
    
    for folder_name, label_id in class_mapping.items():
        files = glob.glob(os.path.join(base_dir, folder_name, '*.npy'))
        for file in files:
            try:
                data_dict = np.load(file, allow_pickle=True).item()
                left = np.squeeze(np.array(data_dict['LeftFrame'])).reshape(60, -1)
                right = np.squeeze(np.array(data_dict['RightFrame'])).reshape(60, -1)
                
                # Combine and Normalize: Scale by max pressure across both feet
                combined = np.hstack((left, right))
                combined = combined / (np.max(combined) + 1e-7) 
                
                all_samples.append(combined)
                all_labels.append(label_id)
            except Exception: continue
                
    return np.array(all_samples), np.array(all_labels)

def build_branch_b_model(input_shape):
    model = models.Sequential([
        layers.Input(shape=input_shape),
        layers.GaussianNoise(0.05), # Adds jitter to sensors to prevent overfitting
        layers.Conv1D(64, kernel_size=3, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
        layers.BatchNormalization(),
        layers.MaxPooling1D(pool_size=2),
        layers.Dropout(0.5), # Harder dropout
        layers.GlobalAveragePooling1D(),
        layers.Dense(32, activation='relu'),
        layers.Dense(3, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

if __name__ == "__main__":
    X, y = load_ieee_plantar_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = build_branch_b_model(input_shape=(60, 3264))
    # Early stopping added to prevent training too long
    early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)
    
    model.fit(X_train, y_train, epochs=30, batch_size=32, 
              validation_data=(X_test, y_test), callbacks=[early_stop])
    
    os.makedirs('models/pretrained', exist_ok=True)
    model.save('models/pretrained/branch_b_biomechanics.h5')