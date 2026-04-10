NervoStep AI 👣

Advanced AI-Driven Plantar Pressure Telemetry & Neuropathy Risk Assessment

NervoStep AI is a clinical-grade diagnostic platform designed to bridge the gap between raw biomechanical sensor data and actionable medical intelligence. By utilizing multimodal deep learning, the platform detects early-stage pressure anomalies to prevent diabetic foot ulcers and neuropathy complications.
🏥 Problem Statement

Diabetic Peripheral Neuropathy (DPN) leads to a loss of protective sensation in the feet. Patients often remain unaware of high-pressure hotspots caused by gait imbalances, leading to:

    Asymptomatic Ulceration: Tissue breakdown that occurs without pain.

    Delayed Diagnosis: Clinical intervention often occurs only after permanent damage.

    High Amputation Rates: Every 20 seconds, a lower limb is lost to diabetes globally.

Current diagnostic tools are often bulky, expensive, and lack predictive AI capabilities to identify risks before physical symptoms appear.
💡 Solution Overview

NervoStep AI provides a preventative "Digital Twin" of foot health. The solution consists of:

    Multimodal Fusion Engine: A deep learning architecture that integrates ECG-derived autonomic markers with a 3,264-point biomechanical sensor array.

    Real-Time Heatmapping: Dynamic SVG visualization of plantar pressure distribution across the forefoot, arch, and heel.

    Predictive Risk Stratification: Automated classification of patient states into Normal, Warning, and Critical with accompanying clinical interventions.

    Longitudinal Monitoring: Tracking of foot temperature variations and risk events to predict "flare-ups" before they occur.

🛠️ Technical Architecture

The platform is built on a robust Python-based stack designed for medical reliability:

    Backend: TensorFlow & Keras (Bi-directional GRU and Fusion Layers)

    Frontend: Streamlit (Optimized for clinical dashboarding)

    Analytics: Plotly, Pandas, NumPy

    Signal Processing: WFDB & NeuroKit2 (Physiological data extraction)

📂 Repository Structure
Plaintext

├── app.py                      # Main dashboard application
├── requirements.txt            # System dependencies
├── nervostep_fusion_core.keras # Production-grade AI model
├── src/
│   ├── data_processor.py       # Sensor data normalization
│   └── explain_ai.py           # SHAP-based clinical transparency
└── assets/                     # UI components and documentation

🚀 Setup & Installation
1. Prerequisites

Ensure you have Python 3.9+ installed. It is recommended to use a virtual environment.
2. Clone the Repository
Bash

git clone https://github.com/yourusername/NervoStep-ai.git
cd NervoStep-ai

3. Install Dependencies
Bash

pip install -r requirements.txt

4. Run Locally
Bash

streamlit run app.py

🔗 Live Demo

Access the production deployment here:

👉 NervoStep.vercel.app (or your Streamlit Cloud URL)
👨‍💻 Developed By

Team NervoTech Developing preventative medical technology through Hardware & Machine Learning.
📄 License

This project is licensed under the MIT License - see the LICENSE file for detail
