import tensorflow as tf
import numpy as np
import shap
import matplotlib.pyplot as plt
import os

def run_dynamic_xai_audit(scenario="RIGHT-RISK"):
    print(f"🤖 --- Initializing NervoStep XAI Reasoning Engine: {scenario} ---")
    
    # 1. Load the production-grade brain
    model_path = 'models/final/nervostep_fusion_core.keras'
    if not os.path.exists(model_path):
        print("❌ Error: Run fusion_model.py first to build the brain.")
        return
    model = tf.keras.models.load_model(model_path)

    # 2. Setup Dynamic Inputs
    # Automatically detect sensor counts to avoid hard-coding
    total_sensors = model.input_shape[1][2] # Detects 3264
    midpoint = total_sensors // 2            # Calculates 1632
    
    test_heart = np.full((1, 60, 1), 0.85)   # Simulating healthy SpO2
    test_feet = np.random.rand(1, 60, total_sensors) * 0.05 # Baseline noise
    
    # 3. Dynamic Simulation Injection
    if scenario == "LEFT-RISK":
        test_feet[0, :, :midpoint] += 0.85
    elif scenario == "RIGHT-RISK":
        test_feet[0, :, midpoint:] += 0.85
    
    # 4. Run AI Inference
    prediction = model.predict([test_heart, test_feet], verbose=0)
    class_idx = np.argmax(prediction[0])
    labels = ["Normal", "Right-Risk", "Left-Risk"] 
    conf = prediction[0][class_idx]
    
    print(f"\n📢 AI ANALYSIS RESULT: {labels[class_idx]} ({conf*100:.1f}% confidence)")

    # 5. SHAP Deep-Dive
    print("🧠 Calculating Feature Importance (SHAP)...")
    bg_heart = np.zeros((5, 60, 1))
    bg_feet = np.zeros((5, 60, total_sensors))
    
    explainer = shap.GradientExplainer(model, [bg_heart, bg_feet])
    shap_values = explainer.shap_values([test_heart, test_feet])
    
    # Extract foot branch [1], sample [0], for the predicted class
    foot_impact = np.abs(shap_values[1][0, :, :, class_idx]).mean(axis=0)

    # 6. Generate Clinical Report
    vitals_score = np.abs(shap_values[0][0, :, :, class_idx]).sum()
    feet_score = foot_impact.sum()
    
    print("\n" + "="*40)
    print("📋 NERVOSTEP CLINICAL EXPLANATION REPORT")
    print("="*40)
    primary = "BIOMECHANICAL" if feet_score > vitals_score else "VASCULAR/AUTONOMIC"
    print(f"💡 PRIMARY INDICATOR: {primary} ASYMMETRY")
    print(f"-> Vitals Influence: {vitals_score:.6f}")
    print(f"-> Foot Influence:   {feet_score:.6f}")
    print("="*40)

    # 7. Dynamic Heatmap Generation
    left_viz = foot_impact[:midpoint].reshape(48, 34)
    right_viz = foot_impact[midpoint:].reshape(48, 34)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    v_max = np.max(foot_impact) + 1e-10
    
    ax1.imshow(left_viz, cmap='hot', vmin=0, vmax=v_max)
    ax1.set_title("Left Foot (SHAP)")
    ax1.axis('off')
    
    ax2.imshow(right_viz, cmap='hot', vmin=0, vmax=v_max)
    ax2.set_title("Right Foot (SHAP)")
    ax2.axis('off')
    
    os.makedirs('reports', exist_ok=True)
    plt.savefig('reports/latest_audit_heatmap.png')
    print("🖼️ Audit Heatmap saved to: reports/latest_audit_heatmap.png")

if __name__ == "__main__":
    # You can change this to "LEFT-RISK" or "NORMAL" to test different states
    run_dynamic_xai_audit(scenario="RIGHT-RISK")