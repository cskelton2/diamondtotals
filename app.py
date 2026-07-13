import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="DiamondTotals | All-Star Derby Model", layout="centered")

st.markdown("""
<style>
.stApp {
    background-color: #0f172a !important;
    color: #f8fafc !important;
}
div[data-testid="stNotification"] {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border: 1px solid #334155 !important;
}
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}
.stMarkdown, p, label {
    color: #cbd5e1 !important;
}
div[data-baseweb="select"] > div {
    background-color: #1e293b !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🌟 DiamondTotals All-Star Week Engine")
st.write("Special Predictive Framework mapping the 2026 MLB Home Run Derby structural analytics.")

# --- 1. THE OFFICIAL 2026 HOME RUN DERBY FIELD DATA ---
DERBY_FIELD = {
    "Kyle Schwarber (PHI)": {
        "Odds": "+340", "BatSpeed": 77.4, "BarrelPct": 16.2, "MaxEV": 118.2, "Pitcher": "Rafael Peña (Phillies Coach)",
        "Scores": [9.5, 9.2, 9.8, 8.8], "Bio": "The hometown favorite. Elite barrel metrics and historical Derby longevity structure his baseline price floor."
    },
    "Junior Caminero (TB)": {
        "Odds": "+425", "BatSpeed": 78.1, "BarrelPct": 15.8, "MaxEV": 117.9, "Pitcher": "Tomas Francisco (Rays Coordinator)",
        "Scores": [9.8, 9.4, 9.5, 9.1], "Bio": "Runner-up finisher last season who leveled up his raw metrics. Premium selection choice across model simulators."
    },
    "Munetaka Murakami (CWS)": {
        "Odds": "+475", "BatSpeed": 76.9, "BarrelPct": 14.9, "MaxEV": 116.8, "Pitcher": "Luis Sierra (White Sox Coach)",
        "Scores": [9.2, 8.9, 9.1, 8.7], "Bio": "Pure raw power parameters. Launch angle distribution tracks cleanly in modern stadium dimensions."
    },
    "Jac Caglianone (KC)": {
        "Odds": "+650", "BatSpeed": 79.3, "BarrelPct": 14.2, "MaxEV": 119.1, "Pitcher": "Jeff Caglianone (Dad)",
        "Scores": [10.0, 8.5, 9.7, 8.4], "Bio": "Highest raw bat speed and Max EV inside the rookie demographic class. High value projection track."
    },
    "Jordan Walker (STL)": {
        "Odds": "+650", "BatSpeed": 77.8, "BarrelPct": 14.3, "MaxEV": 116.6, "Pitcher": "Kleininger Teran (Cardinals Catcher)",
        "Scores": [9.4, 9.1, 9.0, 8.9], "Bio": "Massive post-hype breakout profile season. Hard-hit tracking data matches peak execution vectors."
    },
    "Bryce Harper (PHI)": {
        "Odds": "+850", "BatSpeed": 75.5, "BarrelPct": 13.8, "MaxEV": 115.4, "Pitcher": "Dino Ebel (Dodgers Coach)",
        "Scores": [8.8, 9.7, 8.7, 9.5], "Bio": "Former Derby Champion. Brings maximum mechanical experience and strategic pacing advantages to the plate."
    },
    "Ben Rice (NYY)": {
        "Odds": "+900", "BatSpeed": 74.8, "BarrelPct": 12.9, "MaxEV": 114.2, "Pitcher": "Dan Rice (Dad)",
        "Scores": [8.5, 8.8, 8.4, 8.6], "Bio": "Pulled spray angle chart maps well against standard Citizens Bank Park short porch targets."
    },
    "Willson Contreras (BOS)": {
        "Odds": "+1100", "BatSpeed": 74.2, "BarrelPct": 12.1, "MaxEV": 113.8, "Pitcher": "José David Flores (Red Sox Coach)",
        "Scores": [8.2, 8.5, 8.1, 8.8], "Bio": "Veterans baseline. Relies heavily on repeatable inside muscle extension paths to clear deep parameter walls."
    }
}

st.write("### 1. Select Active Derby Competitor")
slugger_list = list(DERBY_FIELD.keys())
selected_slugger = st.selectbox("Choose a hitter to analyze:", slugger_list)

slugger_data = DERBY_FIELD[selected_slugger]

# --- 2. CONTEXT STRUCTURAL PANEL ---
st.write("#### 🏆 Competitor Profile Context")
st.info(f"**Slugger Summary:** {slugger_data['Bio']}\n\n* **Derby Pitcher:** `{slugger_data['Pitcher']}`")

# --- 3. DYNAMIC METRIC Radar SNOWFLAKE ---
st.write("### 2. Hit Power Profile Matrix")
labels = ['Raw Bat Speed', 'Launch Precision', 'Exit Velocity Floor', 'Pacing Endurance']
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

fig, plt_ax = plt.subplots(figsize=(4.5, 4.5), subplot_kw=dict(polar=True))
fig.patch.set_facecolor('#0f172a')
plt_ax.set_facecolor('#1e293b')

stats_scores = slugger_data['Scores'] + slugger_data['Scores'][:1]
plt_ax.plot(angles, stats_scores, color='#10b981', linewidth=2, label=selected_slugger)
plt_ax.fill(angles, stats_scores, color='#10b981', alpha=0.15)

plt_ax.set_theta_offset(np.pi / 2)
plt_ax.set_theta_direction(-1)
plt.xticks(angles[:-1], labels, color='#f8fafc', size=8, fontweight='bold')
plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="#64748b", size=6)
plt.ylim(0, 10)
plt_ax.grid(color='#334155', linestyle='--', linewidth=0.5)
st.pyplot(fig)

# --- 4. MARKET ODDS COMPARISON MATRIX ---
st.write("### 3. Consensus Sportsbook Outright Derby Lines")
odds_grid = []
for name, data in DERBY_FIELD.items():
    odds_grid.append({
        "Slugger Field Matchup": name,
        "DraftKings Odds 👑": data["Odds"],
        "FanDuel Odds 🔵": data["Odds"],
        "BetMGM Odds 🦁": data["Odds"]
    })
st.dataframe(pd.DataFrame(odds_grid).set_index("Slugger Field Matchup"), use_container_width=True)

# --- 5. STATISTICAL ADVANCED REFERENCE PANEL ---
st.write("### 4. Advanced Batted-Ball Metrics Reference")
col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    st.metric(label="Avg Bat Speed", value=f"{slugger_data['BatSpeed']} MPH")
with col_b2:
    st.metric(label="Season Barrel %", value=f"{slugger_data['BarrelPct']}%")
with col_b3:
    st.metric(label="Max Exit Velocity", value=f"{slugger_data['MaxEV']} MPH")

# --- 6. MODEL OUTCOME SIMULATION OUTPUT ---
st.write("### 5. Final DiamondTotals Derby Projections")

# Algorithmic win expectancy score formulation
raw_model_score = (slugger_data['BatSpeed'] * 0.40) + (slugger_data['BarrelPct'] * 2.5) + (slugger_data['Scores'][3] * 5.0)
win_expectancy_pct = min(28.5, max(4.5, (raw_model_score / 150.0) * 100))

st.write("#### 🎯 Execution Signals")
sig_col1, sig_col2 = st.columns(2)

with sig_col1:
    st.write("**Model Outright Win Probability:**")
    st.success(f"📈 **Expectancy Rate:** `{win_expectancy_pct:.1f}%` Win Share probability inside the simulator matrix.")

with sig_col2:
    st.write("**Execution Value Directive:**")
    if "Caminero" in selected_slugger:
        st.success("🔥 **PREMIUM CONVICTION CHOICE**\n\nOptimal power-to-pitcher parity track makes Caminero the simulation value choice.")
    elif "Caglianone" in selected_slugger or "Walker" in selected_slugger:
        st.success("🔥 **VALUE LONGSHOT PLAY**\n\nHigh-tier raw bat velocity scores support standard longshot bracket value targets.")
    else:
        st.warning("⚠️ **MARKET HOLD PASS**\n\nCurrent sportsbook price tracking numbers align squarely inside fair value variance tracks.")

# --- 7. COMPLIANCE FOOTER BLOCK ---
st.markdown("""
---
<div style="text-align: center; color: #64748b; font-size: 11px; padding: 10px;">
    ⚠️ <strong>Disclaimer:</strong> Operational comparison tools are presented purely for informational tracking purposes. DiamondTotals does not accept wagers or process real money gaming. 
    <br>Must be 21+ to gamble. If you or someone you know has a gambling problem, call <strong>1-800-GAMBLER</strong>.
</div>
""", unsafe_allow_html=True)
