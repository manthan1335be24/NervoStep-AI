import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="NeuroSole Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS focused ONLY on our custom components, leaving Streamlit's native UI intact
st.markdown("""<style>
/* Main Background & Font */
.stApp { background-color: #f4f7f9; }

/* Custom Metric Cards */
.metric-container { display: flex; justify-content: space-between; gap: 20px; margin-bottom: 30px; margin-top: 10px; }
.metric-card {
    background-color: #ffffff; 
    border: 1px solid #e2e8f0; 
    border-radius: 12px;
    padding: 24px; 
    flex: 1; 
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease;
}
.metric-card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
.metric-title { color: #64748b; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
.metric-value { font-size: 2.2rem; font-weight: 800; color: #0f172a; line-height: 1.2; }



/* Clean up top padding */
.block-container { padding-top: 2rem; padding-bottom: 2rem; }
</style>""", unsafe_allow_html=True)

# --- 2. HEADER ---
st.markdown("""<div style="margin-bottom: 30px;">
<h1 style="color: #0f172a; font-size: 2.5rem; font-weight: 900; margin-bottom: 0;">NeuroSole AI</h1>
<p style="color: #64748b; font-size: 1rem; font-weight: 500; margin-top: 5px;">ADVANCED CLINICAL PLANTAR PRESSURE ANALYSIS</p>
</div>""", unsafe_allow_html=True)

# --- 3. MAIN LAYOUT & CONTROLS ---
ctrl_col1, ctrl_col2, _ = st.columns([2, 1, 5])
with ctrl_col1:
    scenario = st.selectbox("Select Patient Scenario", ["Normal", "Warning", "Critical"], label_visibility="collapsed")
with ctrl_col2:
    if st.button("↻ Run Analysis", type="primary", use_container_width=True):
        with st.spinner("Processing sensor arrays..."): time.sleep(0.8)

st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border-color: #e2e8f0;'>", unsafe_allow_html=True)

# --- 4. TABS ---
tab1, tab2 = st.tabs(["📊 Diagnostic Scan", "📈 Clinical Trends"])

# --- TAB 1: AI SCAN ---
with tab1:
    # Logic Engine
    if scenario == "Normal":
        r_text, r_color, high_z, med_z = "Normal", "#10b981", "0", "0"
        region = "Optimal"
        advice = "Pressure distribution is within healthy parameters. Continue routine monitoring."
        glow_fill = "rgba(59, 130, 246, 0.03)" 
        h1_r, h2_r, h3_r = 0, 0, 0 
        hotspot_color = "rgba(0,0,0,0)" 
    elif scenario == "Warning":
        r_text, r_color, high_z, med_z = "Warning", "#f59e0b", "0", "2"
        region = "Mid-foot & Heel"
        advice = "Elevated pressure detected. Suggest reviewing footwear and gait mechanics."
        glow_fill = "rgba(245, 158, 11, 0.08)" 
        h1_r, h2_r, h3_r = 0, 35, 30 
        hotspot_color = "#f59e0b"
    else: # Critical
        r_text, r_color, high_z, med_z = "Critical", "#ef4444", "3", "0"
        region = "Forefoot, Arch & Heel"
        advice = "Critical pressure zones detected. Clinical intervention and orthotic offloading advised immediately."
        glow_fill = "rgba(239, 68, 68, 0.08)" 
        h1_r, h2_r, h3_r = 30, 35, 45 
        hotspot_color = "#ef4444"

    # Metric Cards HTML (Completely left-aligned to fix the ghost box)
    st.markdown(f"""<div class="metric-container">
<div class="metric-card"><div class="metric-title" style="color:{r_color}">Current Risk Level</div><div class="metric-value" style="color:{r_color}">{r_text}</div></div>
<div class="metric-card"><div class="metric-title">High-Risk Zones</div><div class="metric-value">{high_z}</div></div>
<div class="metric-card"><div class="metric-title">Medium-Risk Zones</div><div class="metric-value">{med_z}</div></div>
</div>""", unsafe_allow_html=True)

    # Visual Scan Area
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    v_col1, v_col2 = st.columns([1, 2])
    
    with v_col1:
        st.markdown("<h4 style='color:#0f172a; margin-bottom:20px; font-weight:800; text-align:center;'>Sole Heatmap</h4>", unsafe_allow_html=True)
        
        svg_code = f"""<svg viewBox="0 0 320 550" style="width:100%; max-width:220px; display:block; margin:auto; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.05));">
<defs>
<radialGradient id="heat" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="{hotspot_color}" stop-opacity="0.85" />
<stop offset="100%" stop-color="{hotspot_color}" stop-opacity="0" />
</radialGradient>
<filter id="glow">
<feGaussianBlur stdDeviation="6" result="coloredBlur"/>
<feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
</defs>
<path d="M 80,140 C 80,240 60,340 80,440 C 100,520 190,530 210,470 C 235,400 200,320 230,240 C 260,160 290,165 290,140 C 290,110 120,110 80,140 Z" fill="{glow_fill}" stroke="#cbd5e1" stroke-width="2" />
<ellipse cx="110" cy="80" rx="28" ry="38" fill="{glow_fill}" stroke="#cbd5e1" stroke-width="2"/>
<ellipse cx="175" cy="65" rx="20" ry="32" fill="{glow_fill}" stroke="#cbd5e1" stroke-width="2"/>
<ellipse cx="225" cy="80" rx="16" ry="26" fill="{glow_fill}" stroke="#cbd5e1" stroke-width="2"/>
<ellipse cx="260" cy="105" rx="14" ry="20" fill="{glow_fill}" stroke="#cbd5e1" stroke-width="2"/>
<ellipse cx="285" cy="135" rx="11" ry="16" fill="{glow_fill}" stroke="#cbd5e1" stroke-width="2"/>
<circle cx="110" cy="150" r="{h1_r}" fill="url(#heat)" filter="url(#glow)"/>
<circle cx="150" cy="300" r="{h2_r}" fill="url(#heat)" filter="url(#glow)"/>
<circle cx="150" cy="460" r="{h3_r}" fill="url(#heat)" filter="url(#glow)"/>
</svg>"""
        st.markdown(svg_code, unsafe_allow_html=True)

    with v_col2:
        report_html = f"""<div style="padding: 10px 30px; height: 100%; display: flex; flex-direction: column; justify-content: center;">
<h5 style="color:#2563eb; font-size:0.85rem; font-weight:800; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:15px;">Diagnostic Report</h5>
<div style="background-color: #f8fafc; border-radius: 8px; padding: 15px; margin-bottom: 20px; border-left: 4px solid {r_color};">
<p style="font-size:1rem; margin-bottom:8px; color:#0f172a;"><strong style="color:#64748b;">System Status:</strong> <span style="color:{r_color}; font-weight:700;">{r_text}</span></p>
<p style="font-size:1rem; margin-bottom:0px; color:#0f172a;"><strong style="color:#64748b;">Primary Affection:</strong> <span style="font-weight:600;">{region}</span></p>
</div>
<h6 style="color:#0f172a; font-size:1rem; font-weight:700; margin-bottom:10px;">Recommended Clinical Actions</h6>
<ul style="color:#475569; font-size:1rem; font-weight:500; line-height:1.6; padding-left:20px;">
<li>{advice}</li>
<li>{'Continuous telemetry logged for 24h.' if scenario != 'Normal' else 'No immediate intervention required.'}</li>
</ul>
</div>"""
        st.markdown(report_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: TRENDS ---
with tab2:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0f172a; margin-bottom:20px; font-weight:800;'>Longitudinal Temperature & Risk Telemetry</h4>", unsafe_allow_html=True)
    
    dates = pd.date_range(end=pd.Timestamp.today(), periods=10, freq='D')
    df = pd.DataFrame({
        'Date': dates,
        'Heel Temp': [32, 32.2, 31.8, 32.5, 33, 32.8, 32.1, 32.4, 32.6, 33.1],
        'Toe Temp': [34, 34.5, 34.2, 34.8, 34.1, 34.3, 34.6, 34.4, 34.7, 34.9],
        'Risk Level': [1, 1, 1, 0, 0, 1, 0, 0, 1, 0]
    })

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Heel Temp'], name='Heel Temp (°C)', line=dict(color='#3b82f6', width=3)))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Toe Temp'], name='Toe Temp (°C)', line=dict(color='#94a3b8', width=3)))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Risk Level']*5 + 30, name='Risk Events', line=dict(color='#ef4444', width=3, dash='dot')))

    fig.update_layout(
        plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
        font=dict(color='#475569', family="sans-serif"), 
        margin=dict(l=0, r=0, t=10, b=0), height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor='#f1f5f9', showline=True, linecolor='#cbd5e1'),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9', showline=True, linecolor='#cbd5e1', title="Temperature / Scaled Risk")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)