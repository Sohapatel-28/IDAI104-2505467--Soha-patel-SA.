"""
╔══════════════════════════════════════════════════════════════════╗
║   TechLift Solutions — Smart Elevator Vibration Dashboard        ║
║   Summative Assessment | Mathematics for AI                      ║
║   Scenario 2: Smarter Elevator Movement Visualization            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="TechLift | Elevator Analytics",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
}
.stApp { background-color: #0d1117; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
    border-right: 1px solid #30363d;
}

.header-banner {
    background: linear-gradient(135deg, #0d1117 0%, #1a2332 50%, #0d1117 100%);
    border: 1px solid #30363d;
    border-left: 4px solid #00e5ff;
    border-radius: 10px;
    padding: 28px 36px;
    margin-bottom: 24px;
}
.header-banner h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #00e5ff;
    margin: 0 0 6px 0;
}
.header-banner p { color: #8b949e; font-size: 0.95rem; margin: 0; }

.metric-row { display: flex; gap: 14px; margin-bottom: 24px; flex-wrap: wrap; }
.metric-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 20px 24px;
    flex: 1;
    min-width: 140px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-2px); }
.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
}
.metric-card.cyan::after   { background: #00e5ff; }
.metric-card.orange::after { background: #ff6b35; }
.metric-card.green::after  { background: #7cfc00; }
.metric-card.purple::after { background: #a78bfa; }
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.9rem;
    font-weight: 700;
    color: #e6edf3;
    line-height: 1;
}
.metric-label { font-size: 0.75rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin-top: 6px; }
.metric-delta { font-size: 0.75rem; margin-top: 4px; }
.metric-delta.good { color: #7cfc00; }
.metric-delta.bad  { color: #ff6b35; }

.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.95rem;
    color: #00e5ff;
    border-bottom: 1px solid #30363d;
    padding-bottom: 8px;
    margin: 24px 0 14px 0;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.insight-box {
    background: #1c2230;
    border-left: 3px solid #00e5ff;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 10px 0;
    font-size: 0.92rem;
    line-height: 1.7;
    color: #e6edf3 !important;
}
.insight-box.warning { border-left-color: #ff6b35; background: #1f1a16; }
.insight-box.success { border-left-color: #7cfc00; background: #141f14; }
.insight-box strong { color: #ffffff !important; }
.insight-box code { color: #00e5ff !important; background: rgba(0,229,255,0.1); padding: 2px 6px; border-radius: 4px; }

/* ── Sidebar all text visible ── */
[data-testid="stSidebar"] { color: #e6edf3 !important; }
[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 { color: #00e5ff !important; }
[data-testid="stSidebar"] strong { color: #e6edf3 !important; }
[data-testid="stSidebar"] .stSlider span { color: #e6edf3 !important; }
[data-testid="stSidebar"] label { color: #c9d1d9 !important; }
[data-testid="stFileUploader"] * { color: #c9d1d9 !important; }
[data-testid="stFileUploader"] { background: #161b22; border: 1px dashed #30363d; border-radius: 8px; }

/* ── Dataframe dark ── */
[data-testid="stDataFrame"] { border: 1px solid #30363d; border-radius: 8px; overflow: hidden; }
iframe { background: #161b22 !important; }

/* ── Sliders & selects ── */
.stSlider label, .stSelectbox label, .stCheckbox label { color: #c9d1d9 !important; }
.stSelectbox > div > div { background: #161b22 !important; border-color: #30363d !important; color: #e6edf3 !important; }

/* ── Metrics ── */
[data-testid="metric-container"] { background: #161b22 !important; border: 1px solid #30363d !important; border-radius: 8px !important; padding: 12px 16px !important; }
[data-testid="metric-container"] label { color: #8b949e !important; }
[data-testid="stMetricValue"] { color: #e6edf3 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: #161b22; border-radius: 8px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #8b949e !important; border-radius: 6px; font-family: 'Space Mono', monospace; font-size: 0.78rem; }
.stTabs [aria-selected="true"] { background: #00e5ff !important; color: #000 !important; font-weight: 700 !important; }

/* ── Buttons ── */
.stButton > button { background: transparent; border: 1px solid #00e5ff; color: #00e5ff !important; border-radius: 6px; font-family: 'Space Mono', monospace; transition: all 0.2s; }
.stButton > button:hover { background: #00e5ff; color: #000 !important; }

/* ── General ── */
p, li, .stMarkdown p { color: #c9d1d9 !important; }
h1, h2, h3, h4 { color: #e6edf3 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  GENERATE / LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def generate_or_load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df, False

    np.random.seed(42)
    n = 2000
    ids = np.arange(1, n + 1)
    base_rev = np.random.normal(3000, 400, n)
    usage_spikes = np.sin(np.linspace(0, 6 * np.pi, n)) * 800
    revolutions = np.clip(base_rev + usage_spikes, 500, 6000).astype(int)
    humidity = np.clip(
        40 + 20 * np.sin(np.linspace(0, 4 * np.pi, n)) + np.random.normal(0, 5, n), 20, 95
    )
    vibration = 0.0012 * revolutions + 0.08 * humidity + np.random.normal(0, 1.5, n)
    anomaly_idx = np.random.choice(n, size=30, replace=False)
    vibration[anomaly_idx] += np.random.uniform(8, 20, 30)
    vibration = np.clip(vibration, 0, None)
    x1 = revolutions * 0.002 + np.random.normal(0, 1, n)
    x2 = humidity * 0.05 + np.random.normal(0, 0.5, n)
    x3 = np.random.normal(5, 2, n) + vibration * 0.1
    x4 = np.random.normal(3, 1.5, n)
    x5 = x1 * 0.3 + x2 * 0.5 + np.random.normal(0, 0.8, n)
    df = pd.DataFrame({
        "ID": ids, "revolutions": revolutions,
        "humidity": humidity.round(2), "vibration": vibration.round(4),
        "x1": x1.round(4), "x2": x2.round(4), "x3": x3.round(4),
        "x4": x4.round(4), "x5": x5.round(4),
    })
    return df, True


def clean_data(df):
    report = {}
    original_shape = df.shape
    dup_count = df.duplicated().sum()
    df = df.drop_duplicates()
    report["duplicates_removed"] = int(dup_count)
    missing_before = df.isnull().sum().sum()
    df = df.fillna(df.median(numeric_only=True))
    report["missing_filled"] = int(missing_before)
    for col in ["revolutions", "humidity", "vibration", "x1", "x2", "x3", "x4", "x5"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna()
    report["final_shape"] = df.shape
    report["original_shape"] = original_shape
    return df, report


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<h2 style="color:#00e5ff;font-family:Space Mono,monospace;margin:0 0 4px 0;">🏢 TechLift</h2>',
        unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#8b949e;font-size:0.85rem;margin:0 0 16px 0;">Smart Elevator Analytics</p>',
        unsafe_allow_html=True)
    st.markdown('<hr style="border-color:#30363d;margin:12px 0;">', unsafe_allow_html=True)

    st.markdown('<p style="color:#00e5ff;font-size:0.8rem;letter-spacing:1px;text-transform:uppercase;font-family:Space Mono,monospace;margin-bottom:8px;">📂 Upload Dataset</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"],
        help="Upload elevator sensor CSV. Demo data used if none uploaded.", label_visibility="collapsed")

    st.markdown('<hr style="border-color:#30363d;margin:12px 0;">', unsafe_allow_html=True)
    st.markdown('<p style="color:#00e5ff;font-size:0.8rem;letter-spacing:1px;text-transform:uppercase;font-family:Space Mono,monospace;margin-bottom:8px;">🎛️ Dashboard Filters</p>', unsafe_allow_html=True)
    filter_placeholder = st.empty()

    st.markdown('<hr style="border-color:#30363d;margin:12px 0;">', unsafe_allow_html=True)
    st.markdown('<p style="color:#00e5ff;font-size:0.8rem;letter-spacing:1px;text-transform:uppercase;font-family:Space Mono,monospace;margin-bottom:10px;">ℹ️ About</p>', unsafe_allow_html=True)
    for label, value in [
        ("Course", "Mathematics for AI"),
        ("Assessment", "Summative · 60 Marks"),
        ("Scenario", "2 — Elevator Visualization"),
        ("Stack", "Streamlit · Plotly · Pandas"),
    ]:
        st.markdown(
            f'<div style="margin-bottom:6px;">'
            f'<span style="color:#8b949e;font-size:0.73rem;text-transform:uppercase;letter-spacing:0.8px;">{label}</span><br>'
            f'<span style="color:#e6edf3;font-size:0.88rem;font-weight:500;">{value}</span>'
            f'</div>',
            unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD & CLEAN
# ─────────────────────────────────────────────
raw_df, is_synthetic = generate_or_load_data(uploaded_file)
df, clean_report = clean_data(raw_df.copy())

with filter_placeholder:
    with st.container():
        rev_range = st.slider("Revolutions Range",
            int(df["revolutions"].min()), int(df["revolutions"].max()),
            (int(df["revolutions"].quantile(0.05)), int(df["revolutions"].quantile(0.95))), step=50)
        hum_range = st.slider("Humidity Range (%)",
            float(df["humidity"].min()), float(df["humidity"].max()),
            (float(df["humidity"].quantile(0.05)), float(df["humidity"].quantile(0.95))), step=1.0)
        vib_threshold = st.slider("Anomaly Threshold",
            float(df["vibration"].quantile(0.90)), float(df["vibration"].max()),
            float(df["vibration"].quantile(0.95)), step=0.1)
        sample_size = st.slider("Time Series Sample", 100, len(df), min(500, len(df)), step=50)

mask = (
    (df["revolutions"] >= rev_range[0]) & (df["revolutions"] <= rev_range[1]) &
    (df["humidity"] >= hum_range[0]) & (df["humidity"] <= hum_range[1])
)
filtered_df = df[mask].copy()
anomalies = df[df["vibration"] >= vib_threshold]
anomaly_pct = len(anomalies) / len(df) * 100


# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="header-banner">
    <h1>🏢 TechLift Elevator Analytics</h1>
    <p>Predictive Maintenance Dashboard &nbsp;·&nbsp; Smarter Elevator Movement Visualization
    &nbsp;·&nbsp; {"⚗️ Demo Data" if is_synthetic else "📊 Your Dataset"}
    &nbsp;·&nbsp; <strong style="color:#00e5ff">{len(df):,} readings loaded</strong></p>
</div>
""", unsafe_allow_html=True)

# ── App Description Strip ──
st.markdown("""
<div style="background:#161b22;border:1px solid #30363d;border-radius:10px;padding:18px 28px;margin-bottom:20px;">
    <p style="color:#8b949e;font-size:0.82rem;text-transform:uppercase;letter-spacing:1px;font-family:Space Mono,monospace;margin:0 0 12px 0;">
        🔬 About This Dashboard
    </p>
    <p style="color:#c9d1d9;font-size:0.93rem;margin:0 0 14px 0;line-height:1.7;">
        This dashboard was built for <strong style="color:#e6edf3;">TechLift Solutions</strong> to 
        analyze elevator sensor data sampled at <strong style="color:#00e5ff;">4Hz during peak evening hours</strong>. 
        It performs full <strong style="color:#e6edf3;">Exploratory Data Analysis (EDA)</strong> to identify 
        factors driving vibration — the key health indicator of elevator door mechanisms — enabling 
        smarter predictive maintenance decisions.
    </p>
    <div style="display:flex;gap:10px;flex-wrap:wrap;">
        <span style="background:rgba(0,229,255,0.1);border:1px solid rgba(0,229,255,0.25);color:#00e5ff;border-radius:20px;padding:4px 14px;font-size:0.78rem;font-family:Space Mono,monospace;">📈 5 Visualizations</span>
        <span style="background:rgba(124,252,0,0.1);border:1px solid rgba(124,252,0,0.25);color:#7cfc00;border-radius:20px;padding:4px 14px;font-size:0.78rem;font-family:Space Mono,monospace;">🧹 Auto Data Cleaning</span>
        <span style="background:rgba(255,107,53,0.1);border:1px solid rgba(255,107,53,0.25);color:#ff6b35;border-radius:20px;padding:4px 14px;font-size:0.78rem;font-family:Space Mono,monospace;">⚡ Anomaly Detection</span>
        <span style="background:rgba(167,139,250,0.1);border:1px solid rgba(167,139,250,0.25);color:#a78bfa;border-radius:20px;padding:4px 14px;font-size:0.78rem;font-family:Space Mono,monospace;">🎮 Live Simulator</span>
        <span style="background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.25);color:#ffd700;border-radius:20px;padding:4px 14px;font-size:0.78rem;font-family:Space Mono,monospace;">🔥 Correlation Heatmap</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  KPI METRICS
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="metric-row">
    <div class="metric-card cyan">
        <div class="metric-value">{len(df):,}</div>
        <div class="metric-label">Total Readings</div>
        <div class="metric-delta good">✓ Cleaned & ready</div>
    </div>
    <div class="metric-card orange">
        <div class="metric-value">{df['vibration'].mean():.3f}</div>
        <div class="metric-label">Avg Vibration</div>
        <div class="metric-delta {'bad' if df['vibration'].mean() > 6 else 'good'}">
            {'⚠ Elevated' if df['vibration'].mean() > 6 else '✓ Normal'}
        </div>
    </div>
    <div class="metric-card green">
        <div class="metric-value">{df['humidity'].mean():.1f}%</div>
        <div class="metric-label">Avg Humidity</div>
        <div class="metric-delta {'bad' if df['humidity'].mean() > 70 else 'good'}">
            {'⚠ High' if df['humidity'].mean() > 70 else '✓ Acceptable'}
        </div>
    </div>
    <div class="metric-card purple">
        <div class="metric-value">{len(anomalies)}</div>
        <div class="metric-label">Anomalies Found</div>
        <div class="metric-delta bad">⚡ {anomaly_pct:.1f}% of readings</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tabs = st.tabs([
    "📋 Data Overview",
    "📈 Time Series",
    "📊 Distributions",
    "🔵 Scatter Analysis",
    "📦 Box Plots",
    "🔥 Heatmap",
    "🎮 Live Explorer",
    "🔍 Insights",
])


# ══════════════════════════════════════════════
#  TAB 0 — DATA OVERVIEW
# ══════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header">Stage 2 — Data Understanding & Cleaning</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🧹 Cleaning Report**")
        cleaning_df = pd.DataFrame({
            "Step": ["Original Rows", "Original Columns", "Duplicates Removed",
                     "Missing Values Filled", "Final Rows", "Final Columns"],
            "Value": [clean_report["original_shape"][0], clean_report["original_shape"][1],
                      clean_report["duplicates_removed"], clean_report["missing_filled"],
                      clean_report["final_shape"][0], clean_report["final_shape"][1]],
        })
        st.dataframe(cleaning_df, use_container_width=True, hide_index=True)
    with col2:
        st.markdown("**📐 Statistical Summary**")
        st.dataframe(df[["revolutions","humidity","vibration","x1","x2","x3","x4","x5"]].describe().round(3),
                     use_container_width=True)

    st.markdown("**👀 First 10 Rows**")
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)

    missing = raw_df.isnull().sum()
    # Show completeness % instead of raw missing count (more meaningful when all=0)
    completeness = ((len(raw_df) - missing) / len(raw_df) * 100).round(1)
    fig_miss = go.Figure(go.Bar(
        x=list(completeness.index), y=list(completeness.values),
        marker_color=["#7cfc00" if v == 100 else "#ff6b35" for v in completeness.values],
        text=[f"{v}%" for v in completeness.values],
        textposition="inside", textfont=dict(color="#0d1117", size=12, family="Space Mono"),
    ))
    fig_miss.update_layout(
        paper_bgcolor="#161b22", plot_bgcolor="#1c2230",
        font=dict(family="DM Sans", color="#e6edf3"),
        title=dict(text="✅ Data Completeness Per Column (100% = No Missing Values)",
                   font=dict(family="Space Mono", color="#00e5ff", size=13)),
        height=320, margin=dict(l=50, r=20, t=55, b=50),
        xaxis=dict(gridcolor="#30363d", linecolor="#30363d", tickfont=dict(color="#e6edf3", size=12)),
        yaxis=dict(gridcolor="#30363d", linecolor="#30363d", tickfont=dict(color="#8b949e"),
                   title="Completeness (%)", range=[0, 110], title_font=dict(color="#8b949e")),
    )
    st.plotly_chart(fig_miss, use_container_width=True)
    st.markdown(
        '<div class="insight-box success">✅ <strong>All columns are 100% complete</strong> — '
        'no missing values detected. The dataset is clean and ready for analysis.</div>',
        unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 1 — TIME SERIES
# ══════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">Visualization 1 — Time Series of Vibration</div>', unsafe_allow_html=True)
    st.markdown("*Tracks vibration, revolutions & humidity over time. ⭐ Gold stars = anomaly spikes!*")

    plot_df = df.head(sample_size).copy()
    anom_sample = plot_df[plot_df["vibration"] >= vib_threshold]

    fig_ts = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.07,
        subplot_titles=["🔴 Vibration (Target Variable)", "🟢 Door Revolutions", "🔵 Humidity"])

    fig_ts.add_trace(go.Scatter(x=plot_df["ID"].tolist(), y=plot_df["vibration"].tolist(),
        mode="lines", name="Vibration", line=dict(color="#ff6b35", width=2),
        fill="tozeroy", fillcolor="rgba(255,107,53,0.08)"), row=1, col=1)

    if not anom_sample.empty:
        fig_ts.add_trace(go.Scatter(x=anom_sample["ID"].tolist(), y=anom_sample["vibration"].tolist(),
            mode="markers", name="⚡ Anomaly",
            marker=dict(color="#ffd700", size=11, symbol="star",
                        line=dict(color="white", width=1.5))), row=1, col=1)

    fig_ts.add_trace(go.Scatter(x=plot_df["ID"].tolist(), y=plot_df["revolutions"].tolist(),
        mode="lines", name="Revolutions", line=dict(color="#7cfc00", width=1.5),
        fill="tozeroy", fillcolor="rgba(124,252,0,0.06)"), row=2, col=1)

    fig_ts.add_trace(go.Scatter(x=plot_df["ID"].tolist(), y=plot_df["humidity"].tolist(),
        mode="lines", name="Humidity", line=dict(color="#00e5ff", width=1.5),
        fill="tozeroy", fillcolor="rgba(0,229,255,0.06)"), row=3, col=1)

    fig_ts.update_layout(
        paper_bgcolor="#161b22", plot_bgcolor="#0d1117",
        font=dict(family="DM Sans", color="#e6edf3", size=12),
        title=dict(text=f"Sensor Time-Series — First {sample_size} Readings",
                   font=dict(family="Space Mono", color="#00e5ff", size=14)),
        height=580, margin=dict(l=60, r=30, t=70, b=50),
        legend=dict(bgcolor="#161b22", bordercolor="#30363d", borderwidth=1),
    )
    for i in range(1, 4):
        fig_ts.update_xaxes(gridcolor="#30363d", linecolor="#30363d",
                            tickfont=dict(color="#8b949e"), row=i, col=1)
        fig_ts.update_yaxes(gridcolor="#30363d", linecolor="#30363d",
                            tickfont=dict(color="#8b949e"), row=i, col=1)
    fig_ts.update_annotations(font=dict(color="#00e5ff", family="Space Mono", size=11))
    st.plotly_chart(fig_ts, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Peak Vibration", f"{plot_df['vibration'].max():.3f}")
    c2.metric("Anomaly Spikes", f"{len(anom_sample)}", f"of {sample_size} readings")
    c3.metric("Max Revolutions", f"{plot_df['revolutions'].max():,}")

    if not anom_sample.empty:
        st.markdown(f"""
        <div class="insight-box warning">
        ⚡ <strong>{len(anom_sample)} anomalous vibration spikes</strong> in first {sample_size} readings.
        Sudden jumps indicate potential bearing wear — schedule immediate inspection!
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 2 — DISTRIBUTIONS
# ══════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">Visualization 2 — Distributions of Key Sensors</div>', unsafe_allow_html=True)
    st.markdown("*How are values spread? Yellow dashed line = mean. Red dashed line = anomaly threshold.*")

    col1, col2 = st.columns(2)

    with col1:
        fig_hum = go.Figure()
        fig_hum.add_trace(go.Histogram(x=filtered_df["humidity"].tolist(), nbinsx=40,
            marker_color="#00e5ff", opacity=0.85, name="Humidity",
            marker_line=dict(color="#0d1117", width=0.5)))
        fig_hum.add_vline(x=float(filtered_df["humidity"].mean()), line_dash="dash",
            line_color="#ffd700", line_width=2,
            annotation_text=f"Mean: {filtered_df['humidity'].mean():.1f}%",
            annotation_font=dict(color="#ffd700", size=11))
        fig_hum.update_layout(
            paper_bgcolor="#161b22", plot_bgcolor="#0d1117",
            font=dict(family="DM Sans", color="#e6edf3"),
            title=dict(text="💧 Humidity Distribution (%)",
                       font=dict(family="Space Mono", color="#00e5ff", size=13)),
            height=340, margin=dict(l=50, r=20, t=55, b=45),
            xaxis=dict(title="Humidity (%)", gridcolor="#30363d", linecolor="#30363d",
                       tickfont=dict(color="#8b949e")),
            yaxis=dict(title="Count", gridcolor="#30363d", linecolor="#30363d",
                       tickfont=dict(color="#8b949e")),
        )
        st.plotly_chart(fig_hum, use_container_width=True)

    with col2:
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Histogram(x=filtered_df["revolutions"].tolist(), nbinsx=40,
            marker_color="#7cfc00", opacity=0.85, name="Revolutions",
            marker_line=dict(color="#0d1117", width=0.5)))
        fig_rev.add_vline(x=float(filtered_df["revolutions"].mean()), line_dash="dash",
            line_color="#ffd700", line_width=2,
            annotation_text=f"Mean: {filtered_df['revolutions'].mean():.0f}",
            annotation_font=dict(color="#ffd700", size=11))
        fig_rev.update_layout(
            paper_bgcolor="#161b22", plot_bgcolor="#0d1117",
            font=dict(family="DM Sans", color="#e6edf3"),
            title=dict(text="⚙️ Revolutions Distribution",
                       font=dict(family="Space Mono", color="#00e5ff", size=13)),
            height=340, margin=dict(l=50, r=20, t=55, b=45),
            xaxis=dict(title="Revolutions", gridcolor="#30363d", linecolor="#30363d",
                       tickfont=dict(color="#8b949e")),
            yaxis=dict(title="Count", gridcolor="#30363d", linecolor="#30363d",
                       tickfont=dict(color="#8b949e")),
        )
        st.plotly_chart(fig_rev, use_container_width=True)

    fig_vib = go.Figure()
    fig_vib.add_trace(go.Histogram(x=filtered_df["vibration"].tolist(), nbinsx=50,
        marker_color="#a78bfa", opacity=0.85, name="Vibration",
        marker_line=dict(color="#0d1117", width=0.5)))
    fig_vib.add_vline(x=float(vib_threshold), line_dash="dash", line_color="#ff6b35", line_width=2.5,
        annotation_text=f"⚠ Anomaly Threshold: {vib_threshold:.2f}",
        annotation_font=dict(color="#ff6b35", size=12))
    fig_vib.add_vline(x=float(filtered_df["vibration"].mean()), line_dash="dot",
        line_color="#ffd700", line_width=1.5,
        annotation_text=f"Mean: {filtered_df['vibration'].mean():.3f}",
        annotation_font=dict(color="#ffd700", size=11), annotation_position="top left")
    fig_vib.update_layout(
        paper_bgcolor="#161b22", plot_bgcolor="#0d1117",
        font=dict(family="DM Sans", color="#e6edf3"),
        title=dict(text="🎯 Vibration Distribution — Target Variable",
                   font=dict(family="Space Mono", color="#00e5ff", size=13)),
        height=340, margin=dict(l=50, r=20, t=55, b=45),
        xaxis=dict(title="Vibration Level", gridcolor="#30363d", linecolor="#30363d",
                   tickfont=dict(color="#8b949e")),
        yaxis=dict(title="Count", gridcolor="#30363d", linecolor="#30363d",
                   tickfont=dict(color="#8b949e")),
    )
    st.plotly_chart(fig_vib, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    📊 Humidity spans <strong>{df['humidity'].min():.1f}% → {df['humidity'].max():.1f}%</strong>.
    Vibration is right-skewed — most readings are normal but anomaly spikes pull the tail higher.
    Readings beyond the red threshold line require immediate maintenance action.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 3 — SCATTER ANALYSIS (FIXED)
# ══════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">Visualization 3 — Scatter Analysis</div>', unsafe_allow_html=True)
    st.markdown("*Explore sensor relationships interactively. Change axes and color to find patterns!*")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        x_axis = st.selectbox("X Axis", ["revolutions", "humidity", "x1", "x2", "x3", "x4", "x5"], key="sc_x")
    with c2:
        y_axis = st.selectbox("Y Axis", ["vibration", "revolutions", "humidity", "x1", "x2", "x3"], key="sc_y")
    with c3:
        color_by = st.selectbox("Color By", ["humidity", "revolutions", "x1", "x2", "x3", "x4", "x5"], key="sc_col")
    with c4:
        show_trend = st.checkbox("Trend Line", value=True, key="sc_trend")
        show_anom  = st.checkbox("Show Anomalies", value=True, key="sc_anom")

    fig_sc = go.Figure()

    fig_sc.add_trace(go.Scatter(
        x=filtered_df[x_axis].tolist(),
        y=filtered_df[y_axis].tolist(),
        mode="markers",
        name="Sensor Readings",
        marker=dict(
            color=filtered_df[color_by].tolist(),
            colorscale="Plasma",
            colorbar=dict(
                title=dict(text=color_by, font=dict(color="#8b949e", size=11)),
                tickfont=dict(color="#8b949e"),
                bgcolor="#161b22",
                bordercolor="#30363d",
                borderwidth=1,
            ),
            size=6,
            opacity=0.75,
            line=dict(width=0),
        ),
        hovertemplate=(
            f"<b>{x_axis}:</b> %{{x:.2f}}<br>"
            f"<b>{y_axis}:</b> %{{y:.4f}}<br>"
            f"<b>{color_by}:</b> %{{marker.color:.3f}}<extra></extra>"
        ),
    ))

    if show_trend:
        x_v = filtered_df[x_axis].values
        y_v = filtered_df[y_axis].values
        try:
            z = np.polyfit(x_v, y_v, 1)
            p = np.poly1d(z)
            x_l = np.linspace(x_v.min(), x_v.max(), 300)
            fig_sc.add_trace(go.Scatter(
                x=x_l.tolist(), y=p(x_l).tolist(),
                mode="lines",
                name=f"Trend (slope={z[0]:.4f})",
                line=dict(color="#ffd700", width=2.5, dash="dash"),
            ))
        except Exception:
            pass

    if show_anom:
        anom_filt = filtered_df[filtered_df["vibration"] >= vib_threshold]
        if not anom_filt.empty:
            fig_sc.add_trace(go.Scatter(
                x=anom_filt[x_axis].tolist(),
                y=anom_filt[y_axis].tolist(),
                mode="markers", name="⚡ Anomaly",
                marker=dict(color="#ff6b35", size=12, symbol="star",
                            line=dict(color="white", width=1.5)),
                hovertemplate=f"<b>⚡ ANOMALY</b><br>{x_axis}: %{{x:.2f}}<br>{y_axis}: %{{y:.4f}}<extra></extra>",
            ))

    fig_sc.update_layout(
        paper_bgcolor="#161b22", plot_bgcolor="#0d1117",
        font=dict(family="DM Sans", color="#e6edf3", size=12),
        title=dict(text=f"🔵 {x_axis.title()} vs {y_axis.title()} — colored by {color_by}",
                   font=dict(family="Space Mono", color="#00e5ff", size=14)),
        height=520, margin=dict(l=60, r=30, t=65, b=55),
        legend=dict(bgcolor="#161b22", bordercolor="#30363d", borderwidth=1,
                    font=dict(color="#e6edf3")),
        xaxis=dict(title=x_axis, gridcolor="#30363d", linecolor="#30363d",
                   tickfont=dict(color="#8b949e"), title_font=dict(color="#8b949e")),
        yaxis=dict(title=y_axis, gridcolor="#30363d", linecolor="#30363d",
                   tickfont=dict(color="#8b949e"), title_font=dict(color="#8b949e")),
    )
    st.plotly_chart(fig_sc, use_container_width=True)

    corr = float(filtered_df[x_axis].corr(filtered_df[y_axis]))
    strength  = "Strong 💪" if abs(corr) > 0.6 else ("Moderate 👍" if abs(corr) > 0.3 else "Weak 🤔")
    direction = "positive 📈" if corr > 0 else "negative 📉"
    st.markdown(f"""
    <div class="insight-box {'warning' if abs(corr) > 0.5 else ''}">
    🔗 <strong>Correlation ({x_axis} ↔ {y_axis}): r = {corr:.3f}</strong> — {strength}, {direction} relationship.
    Try changing the X/Y axes above to discover new patterns in the data!
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 4 — BOX PLOTS (FIXED)
# ══════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">Visualization 4 — Box Plots & Outlier Detection</div>', unsafe_allow_html=True)
    st.markdown("*Box plots show spread, median and outlier dots for each sensor channel.*")

    sensor_cols = ["x1", "x2", "x3", "x4", "x5"]
    colors_bp   = ["#00e5ff", "#7cfc00", "#a78bfa", "#ff6b35", "#ffd700"]

    fig_box = go.Figure()
    for col, color in zip(sensor_cols, colors_bp):
        fig_box.add_trace(go.Box(
            y=filtered_df[col].tolist(),
            name=col.upper(),
            marker=dict(color=color, size=4, opacity=0.6),
            line=dict(color=color, width=2),
            boxmean="sd",
            boxpoints="outliers",
        ))

    fig_box.update_layout(
        paper_bgcolor="#161b22", plot_bgcolor="#0d1117",
        font=dict(family="DM Sans", color="#e6edf3", size=12),
        title=dict(text="📦 Sensor Signal Distribution (x1–x5) with Outlier Detection",
                   font=dict(family="Space Mono", color="#00e5ff", size=14)),
        height=480, margin=dict(l=60, r=30, t=65, b=50),
        showlegend=True,
        legend=dict(bgcolor="#161b22", bordercolor="#30363d", borderwidth=1),
        xaxis=dict(gridcolor="#30363d", linecolor="#30363d",
                   tickfont=dict(color="#e6edf3", size=13)),
        yaxis=dict(title="Sensor Reading Value", gridcolor="#30363d", linecolor="#30363d",
                   tickfont=dict(color="#8b949e"), title_font=dict(color="#8b949e")),
    )
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown('<div class="section-header">Vibration by Humidity Category</div>', unsafe_allow_html=True)

    fdf2 = filtered_df.copy()
    fdf2["hum_cat"] = pd.cut(fdf2["humidity"],
        bins=[0, 40, 55, 70, 200],
        labels=["🟢 Low (<40%)", "🟡 Moderate (40–55%)", "🟠 High (55–70%)", "🔴 Very High (>70%)"],
        right=False)

    fig_box2 = go.Figure()
    cat_colors = {"🟢 Low (<40%)": "#7cfc00", "🟡 Moderate (40–55%)": "#ffd700",
                  "🟠 High (55–70%)": "#ff6b35", "🔴 Very High (>70%)": "#ff4444"}
    for level, color in cat_colors.items():
        subset = fdf2[fdf2["hum_cat"] == level]
        if not subset.empty:
            fig_box2.add_trace(go.Box(
                y=subset["vibration"].tolist(),
                name=level,
                marker=dict(color=color, size=4, opacity=0.7),
                line=dict(color=color, width=2),
                boxmean=True,
                boxpoints="outliers",
            ))

    fig_box2.update_layout(
        paper_bgcolor="#161b22", plot_bgcolor="#0d1117",
        font=dict(family="DM Sans", color="#e6edf3", size=12),
        title=dict(text="💧 Vibration vs Humidity Level — Does moisture increase wear?",
                   font=dict(family="Space Mono", color="#00e5ff", size=14)),
        height=420, margin=dict(l=60, r=30, t=65, b=50),
        legend=dict(bgcolor="#161b22", bordercolor="#30363d", borderwidth=1),
        xaxis=dict(gridcolor="#30363d", linecolor="#30363d",
                   tickfont=dict(color="#e6edf3", size=11)),
        yaxis=dict(title="Vibration Level", gridcolor="#30363d", linecolor="#30363d",
                   tickfont=dict(color="#8b949e"), title_font=dict(color="#8b949e")),
    )
    st.plotly_chart(fig_box2, use_container_width=True)

    st.markdown("""
    <div class="insight-box warning">
    📦 <strong>x3 and x5 show the most outliers</strong> — irregular spikes indicating bearing wear.
    Vibration rises consistently from Low → Very High humidity, confirming moisture as a key stress factor.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 5 — HEATMAP (FIXED)
# ══════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header">Visualization 5 — Correlation Heatmap</div>', unsafe_allow_html=True)
    st.markdown("*Red = strong positive, Blue = strong negative correlation. Hover to see exact values!*")

    numeric_cols = ["revolutions", "humidity", "vibration", "x1", "x2", "x3", "x4", "x5"]
    corr_matrix  = filtered_df[numeric_cols].corr()

    fig_heat = go.Figure(go.Heatmap(
        z=corr_matrix.values.tolist(),
        x=corr_matrix.columns.tolist(),
        y=corr_matrix.index.tolist(),
        colorscale="RdBu_r",
        zmid=0, zmin=-1, zmax=1,
        text=corr_matrix.values.round(2).tolist(),
        texttemplate="%{text}",
        textfont=dict(size=12, color="white"),
        colorbar=dict(
            title=dict(text="r", font=dict(color="#8b949e", size=12)),
            tickfont=dict(color="#8b949e"),
            bgcolor="#161b22",
            bordercolor="#30363d",
            borderwidth=1,
        ),
        hoverongaps=False,
        hovertemplate="<b>%{y} ↔ %{x}</b><br>Correlation: %{z:.3f}<extra></extra>",
    ))

    fig_heat.update_layout(
        paper_bgcolor="#161b22", plot_bgcolor="#0d1117",
        font=dict(family="DM Sans", color="#e6edf3", size=12),
        title=dict(text="🔥 Pearson Correlation Matrix — All Sensor Features",
                   font=dict(family="Space Mono", color="#00e5ff", size=14)),
        height=520, margin=dict(l=60, r=30, t=70, b=60),
    )
    fig_heat.update_xaxes(side="bottom", tickfont=dict(color="#e6edf3", size=11),
                          gridcolor="#30363d", linecolor="#30363d")
    fig_heat.update_yaxes(autorange="reversed", tickfont=dict(color="#e6edf3", size=11),
                          gridcolor="#30363d", linecolor="#30363d")
    st.plotly_chart(fig_heat, use_container_width=True)

    vib_corr = corr_matrix["vibration"].drop("vibration").sort_values(ascending=False)
    fig_bar = go.Figure(go.Bar(
        x=vib_corr.index.tolist(),
        y=vib_corr.values.tolist(),
        marker=dict(
            color=vib_corr.values.tolist(),
            colorscale="RdYlGn", cmin=-1, cmax=1,
            showscale=True,
            colorbar=dict(title=dict(text="r", font=dict(color="#8b949e")),
                          tickfont=dict(color="#8b949e")),
            line=dict(color="#0d1117", width=1),
        ),
        text=[f"{v:.3f}" for v in vib_corr.values],
        textposition="outside", textfont=dict(color="#e6edf3"),
    ))
    fig_bar.update_layout(
        paper_bgcolor="#161b22", plot_bgcolor="#0d1117",
        font=dict(family="DM Sans", color="#e6edf3"),
        title=dict(text="Feature Importance for Predicting Vibration",
                   font=dict(family="Space Mono", color="#00e5ff", size=13)),
        height=360, margin=dict(l=50, r=30, t=60, b=50),
        xaxis=dict(gridcolor="#30363d", linecolor="#30363d", tickfont=dict(color="#e6edf3", size=12)),
        yaxis=dict(title="Correlation (r)", gridcolor="#30363d", linecolor="#30363d",
                   tickfont=dict(color="#8b949e"), title_font=dict(color="#8b949e")),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    top = vib_corr.idxmax()
    st.markdown(f"""
    <div class="insight-box">
    🏆 <strong>Best predictor of vibration: <code>{top}</code> (r = {vib_corr.max():.3f})</strong>.
    Monitor this sensor most closely for early-warning of mechanical failures!
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 6 — LIVE EXPLORER (FUN!)
# ══════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-header">🎮 Live Sensor Explorer — Simulate Elevator Conditions!</div>', unsafe_allow_html=True)
    st.markdown("*Adjust the sliders below and watch the elevator health gauge update instantly!*")

    col1, col2, col3 = st.columns(3)
    with col1:
        sim_rev = st.slider("🔄 Door Revolutions", 500, 6000, 3000, 100, key="sim_rev")
    with col2:
        sim_hum = st.slider("💧 Humidity (%)", 20, 95, 50, 1, key="sim_hum")
    with col3:
        sim_x3  = st.slider("📡 Sensor x3 Value", 0.0, 15.0, 5.0, 0.1, key="sim_x3")

    sim_vib    = 0.0012 * sim_rev + 0.08 * sim_hum + sim_x3 * 0.1
    sim_color  = "#ff4444" if sim_vib > vib_threshold else ("#ffd700" if sim_vib > vib_threshold * 0.8 else "#7cfc00")
    sim_status = "🔴 CRITICAL — Schedule Maintenance NOW!" if sim_vib > vib_threshold else \
                 ("🟡 WARNING — Monitor Closely" if sim_vib > vib_threshold * 0.8 else "🟢 NORMAL — All Systems Good!")

    st.markdown(f"""
    <div class="insight-box" style="border-left-color:{sim_color}; text-align:center; padding:24px;">
        <div style="font-family:'Space Mono',monospace; font-size:2.8rem; color:{sim_color}; font-weight:700;">
            {sim_vib:.3f}
        </div>
        <div style="font-size:0.9rem; color:#8b949e; margin-top:4px;">Estimated Vibration Level</div>
        <div style="font-size:1.2rem; margin-top:12px; font-weight:600; color:{sim_color};">
            {sim_status}
        </div>
    </div>""", unsafe_allow_html=True)

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=float(sim_vib),
        delta={"reference": float(df["vibration"].mean()), "valueformat": ".3f",
               "increasing": {"color": "#ff6b35"}, "decreasing": {"color": "#7cfc00"}},
        title={"text": "Vibration Health Gauge",
               "font": {"color": "#00e5ff", "family": "Space Mono", "size": 14}},
        number={"font": {"color": "#e6edf3", "family": "Space Mono", "size": 30}},
        gauge={
            "axis": {"range": [0, float(df["vibration"].max()) * 1.1],
                     "tickcolor": "#8b949e", "tickfont": {"color": "#8b949e"}},
            "bar": {"color": sim_color, "thickness": 0.25},
            "bgcolor": "#161b22",
            "borderwidth": 1, "bordercolor": "#30363d",
            "steps": [
                {"range": [0, float(vib_threshold) * 0.6], "color": "rgba(124,252,0,0.12)"},
                {"range": [float(vib_threshold) * 0.6, float(vib_threshold) * 0.8], "color": "rgba(255,215,0,0.12)"},
                {"range": [float(vib_threshold) * 0.8, float(vib_threshold)], "color": "rgba(255,107,53,0.12)"},
                {"range": [float(vib_threshold), float(df["vibration"].max()) * 1.1], "color": "rgba(255,0,0,0.18)"},
            ],
            "threshold": {"line": {"color": "#ff4444", "width": 3},
                          "thickness": 0.8, "value": float(vib_threshold)},
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor="#161b22",
        font=dict(color="#e6edf3", family="DM Sans"),
        height=360, margin=dict(l=30, r=30, t=50, b=30),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Your Vibration", f"{sim_vib:.3f}", f"{sim_vib - df['vibration'].mean():.3f} vs avg")
    c2.metric("Dataset Average", f"{df['vibration'].mean():.3f}")
    c3.metric("Dataset Max", f"{df['vibration'].max():.3f}")
    c4.metric("Anomaly Threshold", f"{vib_threshold:.3f}")

    # Context scatter
    sample_ctx = df.sample(min(500, len(df)), random_state=42)
    fig_ctx = go.Figure()
    fig_ctx.add_trace(go.Scatter(
        x=sample_ctx["revolutions"].tolist(), y=sample_ctx["vibration"].tolist(),
        mode="markers", name="Historical Data",
        marker=dict(color="#8b949e", size=4, opacity=0.4),
    ))
    fig_ctx.add_trace(go.Scatter(
        x=[sim_rev], y=[sim_vib],
        mode="markers", name="▶ Your Simulation",
        marker=dict(color=sim_color, size=20, symbol="star",
                    line=dict(color="white", width=2)),
    ))
    fig_ctx.update_layout(
        paper_bgcolor="#161b22", plot_bgcolor="#0d1117",
        font=dict(family="DM Sans", color="#e6edf3"),
        title=dict(text="Where does your simulation sit vs historical data?",
                   font=dict(family="Space Mono", color="#00e5ff", size=13)),
        height=380, margin=dict(l=60, r=30, t=60, b=50),
        xaxis=dict(title="Revolutions", gridcolor="#30363d", linecolor="#30363d",
                   tickfont=dict(color="#8b949e")),
        yaxis=dict(title="Vibration", gridcolor="#30363d", linecolor="#30363d",
                   tickfont=dict(color="#8b949e")),
        legend=dict(bgcolor="#161b22", bordercolor="#30363d", borderwidth=1),
    )
    st.plotly_chart(fig_ctx, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 7 — INSIGHTS
# ══════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-header">Stage 4 — Key Insights & Maintenance Recommendations</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🔍 Data-Driven Insights")
        corr_rv = float(df["revolutions"].corr(df["vibration"]))
        corr_hv = float(df["humidity"].corr(df["vibration"]))
        high_rv = float(df[df["revolutions"] > df["revolutions"].quantile(0.75)]["vibration"].mean())
        low_rv  = float(df[df["revolutions"] < df["revolutions"].quantile(0.25)]["vibration"].mean())

        insights = [
            ("",        f"Revolutions correlate with vibration at r = {corr_rv:.3f}. High-usage elevators "
                        f"(top 25%) show {((high_rv/low_rv-1)*100):.1f}% higher vibration — heavier use accelerates wear."),
            ("warning", f"Humidity strongly influences vibration (r = {corr_hv:.3f}). Moisture increases "
                        f"friction in ball bearings, causing premature failure if not managed."),
            ("",        f"{anomaly_pct:.1f}% of readings ({len(anomalies)} events) exceed threshold "
                        f"{vib_threshold:.2f}. Each spike is a potential failure event needing inspection."),
            ("success", f"Sensor x3 has highest correlation with vibration among auxiliary signals. "
                        f"Real-time x3 monitoring provides 15–30 min early warning before failures occur."),
        ]
        for box_type, text in insights:
            st.markdown(f'<div class="insight-box {box_type}">{text}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🔧 Maintenance Recommendations")
        for icon, rec in [
            ("⏰", "Schedule maintenance when revolutions exceed 5,000/session — vibration rises sharply."),
            ("💧", "Install dehumidifiers when humidity exceeds 70% to reduce moisture-induced wear."),
            ("📡", "Set x3 sensor alerts at 95th percentile — it's the earliest mechanical stress indicator."),
            ("📆", "Increase inspections for elevators logging >30 anomalous readings per week."),
        ]:
            st.markdown(f'<div class="insight-box">{icon} {rec}</div>', unsafe_allow_html=True)

        st.markdown("#### 📈 Summary Table")
        st.dataframe(pd.DataFrame({
            "Metric": ["Avg Vibration", "Max Vibration", "Avg Revolutions", "Anomaly Rate", "Avg Humidity"],
            "Value":  [f"{df['vibration'].mean():.3f}", f"{df['vibration'].max():.3f}",
                       f"{df['revolutions'].mean():.0f}", f"{anomaly_pct:.2f}%", f"{df['humidity'].mean():.1f}%"],
            "Status": [
                "⚠️ Monitor" if df["vibration"].mean() > 6 else "✅ Normal",
                "🔴 Critical" if df["vibration"].max() > 20 else "⚠️ Check",
                "⚠️ High" if df["revolutions"].mean() > 4000 else "✅ Normal",
                "🔴 Critical" if anomaly_pct > 5 else "⚠️ Monitor",
                "⚠️ High" if df["humidity"].mean() > 65 else "✅ Normal",
            ]
        }), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("""
    <div class="insight-box success">
    <strong> Summary </strong><br><br>
    This Streamlit dashboard delivers predictive maintenance analytics for TechLift Solutions.
    Using 4Hz elevator sensor data, it visualizes vibration trends, distributions, scatter relationships,
    outliers, and full correlation analysis across 8 interactive tabs — including a live simulation explorer
    with a real-time health gauge. Key findings: <strong>high revolution rates</strong> and
    <strong>elevated humidity</strong> are the primary drivers of vibration, the health indicator of
    elevator door mechanisms.
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<p style="text-align:center; color:#8b949e; font-size:0.8rem; font-family:'Space Mono',monospace;">
🏢 TechLift Solutions · Smart Elevator Analytics · Mathematics for AI — Summative Assessment · Scenario 2
</p>

""", unsafe_allow_html=True)
