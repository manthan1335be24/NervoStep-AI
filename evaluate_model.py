import tensorflow as tf
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import os

def evaluate_nervostep():
    print("📋 Generating Detailed Accuracy Report...")
    
    # 1. Load the strongest branch (Branch B - Feet)
    model_path = 'models/pretrained/branch_b_biomechanics.h5'
    if not os.path.exists(model_path):
        print("❌ Model not found. Please run train_branch_b.py first.")
        return
    
    model = tf.keras.models.load_model(model_path)

    # 2. We need to evaluate it against real data. 
    # For this report, we will re-load the dataset to see how it handles the whole group.
    from train_branch_b import load_ieee_plantar_data
    X, y = load_ieee_plantar_data()
    
    # 3. Get the AI's "Guesses"
    predictions = model.predict(X)
    y_pred = np.argmax(predictions, axis=1)

    # 4. The Final Report
    target_names = ['Normal', 'Left-Risk', 'Right-Risk']
    print("\n" + "="*50)
    print("NERVOSTEP BRAIN: PERFORMANCE METRICS")
    print("="*50)
    print(classification_report(y, y_pred, target_names=target_names))
    
    print("\n--- Confusion Matrix (Where the AI gets confused) ---")
    print("Rows = Actual Class | Columns = AI Guess")
    print(confusion_matrix(y, y_pred))
    print("="*50)

if __name__ == "__main__":
    evaluate_nervostep()