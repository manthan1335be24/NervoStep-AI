import tensorflow as tf
import os
from tensorflow.keras import layers, models

# Import the original build functions so we have the exact same architecture
from train_branch_a import build_branch_a_model
from train_branch_b import build_branch_b_model

def build_fusion_model():
    print("🔗 Linking Branch A (Heart) and Branch B (Feet) using Weight-Transfer...")
    
    # 1. Build fresh models with unique names
    # Branch A
    branch_a_fresh = build_branch_a_model(input_shape=(60, 1))
    branch_a_fresh._name = "heart_expert_branch"
    for i, layer in enumerate(branch_a_fresh.layers):
        layer._name = f"heart_layer_{i}"
        
    # Branch B
    branch_b_fresh = build_branch_b_model(input_shape=(60, 3264))
    branch_b_fresh._name = "foot_expert_branch"
    for i, layer in enumerate(branch_b_fresh.layers):
        layer._name = f"foot_layer_{i}"

    # 2. Load the learned intelligence into these fresh skeletons
    try:
        branch_a_fresh.load_weights('models/pretrained/branch_a_vitals.h5')
        branch_b_fresh.load_weights('models/pretrained/branch_b_biomechanics.h5')
        print("✅ Weights loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading weights: {e}")
        return None

    # 3. Define the Global Inputs
    input_a = layers.Input(shape=(60, 1), name="vitals_input_final")
    input_b = layers.Input(shape=(60, 3264), name="biomechanics_input_final")

    # 4. Route through the experts
    # We take the output before the final classification layer (layers[-2])
    out_a = branch_a_fresh(input_a)
    out_b = branch_b_fresh(input_b)

    # 5. Fusion Decision Core
    combined = layers.Concatenate(name="fusion_junction")([out_a, out_b])
    
    x = layers.Dense(64, activation='relu', name="fusion_dense_1")(combined)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(32, activation='relu', name="fusion_dense_2")(x)
    
    # Final Decision: 3 Classes
    prediction = layers.Dense(3, activation='softmax', name='nervostep_risk_output')(x)

    # 6. Create Model
    full_model = models.Model(inputs=[input_a, input_b], outputs=prediction)
    full_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    return full_model

if __name__ == "__main__":
    nervostep_ai = build_fusion_model()
    if nervostep_ai:
        nervostep_ai.summary()
        os.makedirs('models/final', exist_ok=True)
        nervostep_ai.save('models/final/nervostep_fusion_core.keras')
        print("\n🏆 SUCCESS: The NervoStep Fusion Model is officially unified!")