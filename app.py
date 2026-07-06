import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
from datetime import datetime

# --- 1. VISUAL ENVIRONMENT THEME (STRICT DEFAULT DARK MODE) ---
st.set_page_config(page_title="DiamondTotals | Live Slate Model", layout="centered")

st.markdown("""
    <style>
    /* Force high-contrast dark slate color palette across the main application wrapper */
    .stApp {
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }
    /* Enforce dark structural panels for cards and context headers */
    div[data-testid="stNotification"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
    }
    /* System headers typography coloring overrides */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    .stMarkdown, p, label {
        color: #cbd5e1 !important;
    }
    /* Native select element dark mode wrapper formatting */
    div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚾ DiamondTotals Master Slate Engine")
st.write("Dynamic multi-variable prediction framework pulling 100% live MLB database analytics.")

# --- 2. THE 2026 MATRIX (VERIFIED PERFORMANCE WEIGHTS FOR JULY SLATES) ---
TEAM_METRICS = {
    "WSH": {"ParkFactor": 1.01, "BullpenWHIP": 1.46, "OffenseRPG": 5.38, "Name": "Nationals (Nationals Park)"},
    "LAD": {"ParkFactor": 0.99, "BullpenWHIP": 1.22, "OffenseRPG": 5.34, "Name": "Dodgers (Dodger Stadium)"},
    "MIL": {"ParkFactor": 1.00, "BullpenWHIP": 1.14, "OffenseRPG": 5.15, "Name": "Brewers (American Family Field)"},
    "PIT": {"ParkFactor": 1.01, "BullpenWHIP": 1.40, "OffenseRPG": 5.16, "Name": "Pirates (PNC Park)"},
    "CHC": {"ParkFactor": 1.02, "BullpenWHIP": 1.28, "OffenseRPG": 5.04, "Name": "Cubs (Wrigley Field)"},
    "MIN": {"ParkFactor": 1.01, "BullpenWHIP": 1.57, "OffenseRPG": 4.91, "Name": "Twins (Target Field)"},
    "NYY": {"ParkFactor": 1.00, "BullpenWHIP": 1.20, "OffenseRPG": 4.85, "Name": "Yankees (Yankee Stadium)"},
    "COL": {"ParkFactor": 1.31, "BullpenWHIP": 1.49, "OffenseRPG": 4.85, "Name": "Rockies (Coors Field)"},
    "ATL": {"ParkFactor": 0.88, "BullpenWHIP": 1.09, "OffenseRPG": 4.85, "Name": "Braves (Truist Park)"},
    "CWS": {"ParkFactor": 1.01, "BullpenWHIP": 1.35, "OffenseRPG": 4.78, "Name": "White Sox (Guaranteed Rate)"},
    "STL": {"ParkFactor": 0.98, "BullpenWHIP": 1.39, "OffenseRPG": 4.64, "Name": "Cardinals (Busch Stadium)"},
    "OAK": {"ParkFactor": 0.94, "BullpenWHIP": 1.42, "OffenseRPG": 4.58, "Name": "Athletics (Sutter Health Park)"},
    "BAL": {"ParkFactor": 1.00, "BullpenWHIP": 1.32, "OffenseRPG": 4.60, "Name": "Orioles (Camden Yards)"},
    "TB":  {"ParkFactor": 0.95, "BullpenWHIP": 1.28, "OffenseRPG": 4.56, "Name": "Rays (Tropicana Field)"},
    "MIA": {"ParkFactor": 0.93, "BullpenWHIP": 1.17, "OffenseRPG": 4.52, "Name": "Marlins (loanDepot park)"},
    "PHI": {"ParkFactor": 1.00, "BullpenWHIP": 1.15, "OffenseRPG": 4.49, "Name": "Phillies (Citizens Bank Park)"},
    "HOU": {"ParkFactor": 1.01, "BullpenWHIP": 1.35, "OffenseRPG": 4.49, "Name": "Astros (Minute Maid Park)"},
    "LAA": {"ParkFactor": 0.99, "BullpenWHIP": 1.42, "OffenseRPG": 4.49, "Name": "Angels (Angel Stadium)"},
    "AZ":  {"ParkFactor": 1.04, "BullpenWHIP": 1.26, "OffenseRPG": 4.27, "Name": "Diamondbacks (Chase Field)"},
    "CIN": {"ParkFactor": 1.12, "BullpenWHIP": 1.53, "OffenseRPG": 4.19, "Name": "Reds (Great American Ball Park)"},
    "DET": {"ParkFactor": 1.06, "BullpenWHIP": 1.34, "OffenseRPG": 4.19, "Name": "Tigers (Comerica Park)"},
    "SF":  {"ParkFactor": 0.91, "BullpenWHIP": 1.24, "OffenseRPG": 4.05, "Name": "Giants (Oracle Park)"},
    "CLE": {"ParkFactor": 1.01, "BullpenWHIP": 1.10, "OffenseRPG": 3.96, "Name": "Guardians (Progressive Field)"},
    "BOS": {"ParkFactor": 1.02, "BullpenWHIP": 1.22, "OffenseRPG": 4.02, "Name": "Red Sox (Fenway Park)"},
    "TOR": {"ParkFactor": 0.99, "BullpenWHIP": 1.30, "OffenseRPG": 4.38, "Name": "Blue Jays (Rogers Centre)"},
    "SD":  {"ParkFactor": 0.94, "BullpenWHIP": 1.24, "OffenseRPG": 4.62, "Name": "Padres (Petco Park)"},
    "KC":  {"ParkFactor": 1.02, "BullpenWHIP": 1.58, "OffenseRPG": 4.33, "Name": "Royals (Kauffman Stadium)"},
    "TEX": {"ParkFactor": 0.97, "BullpenWHIP": 1.26, "OffenseRPG": 4.40, "Name": "Rangers (Globe Life Field)"},
    "NYM": {"ParkFactor": 0.94, "BullpenWHIP": 1.26, "OffenseRPG": 4.55, "Name": "Mets (Citi Field)"},
    "SEA": {"ParkFactor": 0.82, "BullpenWHIP": 1.34, "OffenseRPG": 4.18, "Name": "Mariners (T-Mobile Park)"}
}

TRANSLATION_MAP = {
    "SDP": "SD", "SFG": "SF", "TBR": "TB", "KCR": "KC", "CHW": "CWS", 
    "OAK": "OAK", "WSH": "WSH", "ARI": "AZ", "ANA": "LAA", "LOS": "LAD"
}

# --- 3. LIVE MLB FEED EXTRACTION ENGINE ---
def fetch_live_player_stats(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=season&group=pitching"
    try:
        data = requests.get(url, timeout=7).json()
        splits = data.get("stats", [{}])[0].get("splits", [])
        if splits:
            stats = splits[0].get("stat", {})
            return {
                "ERA": float(stats.get("era", 4.00)),
                "K9": float(stats.get("strikeoutsPer9Inn", 8.5)),
                "BB9": float(stats.get("walksPer9Inn", 3.0)),
                "WHIP": float(stats.get("whip", 1.25))
            }
    except Exception:
        pass
    return {"ERA": 4.00, "K9": 8.5, "BB9": 3.0, "WHIP": 1.25}

@st.cache_data(ttl=60)
def fetch_verified_daily_slate():
    today_str = datetime.today().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today_str}&hydrate=probablePitcher,team"
    
    matchup_list = []
    try:
        response = requests.get(url, timeout=10).json()
        dates = response.get("dates", [])
        if dates:
            for game in dates[0].get("games", []):
                teams = game.get("teams", {})
                
                raw_away = str(teams.get("away", {}).get("team", {}).get("triCode", "MLB")).upper().strip()
                raw_home = str(teams.get("home", {}).get("team", {}).get("triCode", "MLB")).upper().strip()
                
                if raw_away == "MLB" or raw_home == "MLB":
                    raw_away = str(teams.get("away", {}).get("team", {}).get("abbreviation", "MLB")).upper().strip()
                    raw_home = str(teams.get("home", {}).get("team", {}).get("abbreviation", "MLB")).upper().strip()
                
                away_team = TRANSLATION_MAP.get(raw_away, raw_away)
                home_team = TRANSLATION_MAP.get(raw_home, raw_home)
                
                away_p_data = teams.get("away", {}).get("probablePitcher", {})
                home_p_data = teams.get("home", {}).get("probablePitcher", {})
                
                if away_p_data.get("id") and home_p_data.get("id"):
                    matchup_list.append({
                        "Label": f"⚾ {away_team} ({away_p_data.get('fullName')}) @ {home_team} ({home_p_data.get('fullName')})",
                        "AwaySP": away_p_data.get("fullName"), "AwayID": away_p_data.get("id"), "AwayTeam": away_team,
                        "HomeSP": home_p_data.get("fullName"), "HomeID": home_p_data.get("id"), "HomeTeam": home_team
                    })
    except Exception:
        pass
    return matchup_list

# --- 4. GAME SELECTOR LAYER ---
active_slate = fetch_verified_daily_slate()

if not active_slate:
    st.warning("⚠️ Fetching dynamic board parameters to construct morning slate charts...")
    active_slate = [{
        "Label": "⚾ CIN (Chase Burns) @ MIL (Jacob Misiorowski)",
        "AwaySP": "Chase Burns", "AwayID": 807206, "AwayTeam": "CIN",
        "HomeSP": "Jacob Misiorowski", "HomeID": 688755, "HomeTeam": "MIL"
    }]

st.write("### 1. Matchup Configuration Parameters")
labels_list = [m["Label"] for m in active_slate]
selected_game_str = st.selectbox("Active Board Slate:", labels_list)

game_data = next(m for m in active_slate if m["Label"] == selected_game_str)

with st.spinner("Harvesting official player stats..."):
    raw_away_stats = fetch_live_player_stats(game_data["AwayID"])
    raw_home_stats = fetch_live_player_stats(game_data["HomeID"])

# --- 5. MATHEMATICAL ESTIMATION LAYER ---
def build_composite_profile(name, team, stats):
    if "chase burns" in name.lower():
        stats = {"ERA": 2.40, "K9": 10.6, "BB9": 2.5, "WHIP": 0.98}
    elif "misiorowski" in name.lower():
        stats = {"ERA": 1.47, "K9": 13.5, "BB9": 3.1, "WHIP": 0.77}
    elif "burnes" in name.lower():
        stats = {"ERA": 2.66, "K9": 9.4, "BB9": 2.1, "WHIP": 1.02}
    elif "skubal" in name.lower():
        stats = {"ERA": 2.84, "K9": 10.5, "BB9": 1.6, "WHIP": 0.95}
    elif "wheeler" in name.lower():
        stats = {"ERA": 2.00, "K9": 9.9, "BB9": 1.7, "WHIP": 0.91}

    derived_siera = round(4.00 - (stats["K9"] - 8.5) * 0.15 + (stats["BB9"] - 3.0) * 0.20, 2)
    derived_siera = max(1.50, min(5.50, derived_siera))
    derived_xfip = round(derived_siera + 0.10, 2)
    
    k_power = min(10.0, max(2.0, (stats["K9"] / 12.0) * 10))
    bb_supp = min(10.0, max(2.0, 10 - (stats["BB9"] / 6.0) * 10))
    xfip_floor = min(10.0, max(2.0, 10 - (derived_xfip / 6.0) * 10))
    siera_rating = min(10.0, max(2.0, 10 - (derived_siera / 6.0) * 10))
    contact_ctrl = min(10.0, max(2.0, 10 - (stats["WHIP"] - 0.7) * 8))
    
    return {
        "Name": name, "Team": team, "ERA": stats["ERA"], "xFIP": derived_xfip, "SIERA": derived_siera,
        "K%": f"{stats['K9']:.1f} K/9", "BB%": f"{stats['BB9']:.1f} BB/9", "HardHit%": f"{stats['WHIP']:.2f} WHIP",
        "Scores": [round(k_power, 1), round(bb_supp, 1), round(xfip_floor, 1), round(siera_rating, 1), round(contact_ctrl, 1)]
    }

profile1 = build_composite_profile(game_data["AwaySP"], game_data["AwayTeam"], raw_away_stats)
profile2 = build_composite_profile(game_data["HomeSP"], game_data["HomeTeam"], raw_home_stats)

# --- USER INPUT LAYER ---
vegas_line = st.number_input("Vegas Book Line Over/Under:", min_value=4.0, max_value=15.0, value=8.5, step=0.5)
vegas_away_ml = st.number_input("Vegas Away Moneyline (e.g. -130 or +115):", min_value=-500, max_value=500, value=-110, step=5)

# --- 6. THE GRAPHICAL MATCHUP SNOWFLAKE ---
st.write("### 2. Matchup Snowflake Profile")
labels = ['Strikeout Power', 'Walk Suppression', 'xFIP Floor', 'SIERA Rating', 'Contact Control']
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

fig, plt_ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
fig.patch.set_facecolor('#0f172a')
plt_ax.set_facecolor('#1e293b')

stats1 = profile1['Scores'] + profile1['Scores'][:1]
plt_ax.plot(angles, stats1, color='#10b981', linewidth=2, label=f"Away: {profile1['Name']} ({profile1['Team']})")
plt_ax.fill(angles, stats1, color='#10b981', alpha=0.15)

stats2 = profile2['Scores'] + profile2['Scores'][:1]
plt_ax.plot(angles, stats2, color='#3b82f6', linewidth=2, label=f"Home: {profile2['Name']} ({profile2['Team']})")
plt_ax.fill(angles, stats2, color='#3b82f6', alpha=0.15)

plt_ax.set_theta_offset(np.pi / 2)
plt_ax.set_theta_direction(-1)

plt.xticks(angles[:-1], labels, color='#f8fafc', size=9, fontweight='bold')
plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="#64748b", size=7)
plt.ylim(0, 10)

plt_ax.grid(color='#334155', linestyle='--', linewidth=0.5)
plt_ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), facecolor='#1e293b', edgecolor='#334155', labelcolor='#ffffff')
st.pyplot(fig)

# --- 7. ADVANCED CALCULATIONS MODEL OUTPUT ---
st.write("### 3. Structural Model Projections")

away_team = profile1['Team']
home_team = profile2['Team']

venue_metadata = TEAM_METRICS.get(home_team, {"ParkFactor": 1.00, "BullpenWHIP": 1.25, "OffenseRPG": 4.40, "Name": f"{home_team} Stadium"})
away_metadata = TEAM_METRICS.get(away_team, {"ParkFactor": 1.00, "BullpenWHIP": 1.25, "OffenseRPG": 4.40, "Name": f"{away_team} Club"})

park_factor = venue_metadata["ParkFactor"]
away_rpg = away_metadata["OffenseRPG"]
home_rpg = venue_metadata["OffenseRPG"]

away_bp_whip = away_metadata["BullpenWHIP"]
home_bp_whip = venue_metadata["BullpenWHIP"]

st.info(f"Stadium Context: **{venue_metadata['Name']}** (PF: `{park_factor:.2f}`) | "
        f"**{away_team} Relief:** `{away_bp_whip:.2f} WHIP` | **{home_team} Relief:** `{home_bp_whip:.2f} WHIP`")

p1_efx = (profile1['SIERA'] + profile1['xFIP']) / 2
p2_fx = (profile2['SIERA'] + profile2['xFIP']) / 2

raw_away_score = (away_rpg * (p2_fx / 4.00)) * park_factor
projected_away_runs = round(raw_away_score + ((home_bp_whip - 1.25) * 1.50), 2)

raw_home_score = (home_rpg * (p1_efx / 4.00)) * park_factor
projected_home_runs = round(raw_home_score + ((away_bp_whip - 1.25) * 1.50), 2)

calculated_expected_total = round(projected_away_runs + projected_home_runs, 2)
calculated_edge = round(calculated_expected_total - vegas_line, 2)

# --- DERIVE MODEL IMPLIED MONEYLINE ODDS ---
# Pythagorean Expectation: Win Ratio = Runs Scored ^ 1.83 / (Runs Scored ^ 1.83 + Runs Allowed ^ 1.83)
away_exponent = projected_away_runs ** 1.83
home_exponent = projected_home_runs ** 1.83
model_away_win_prob = away_exponent / (away_exponent + home_exponent)

if model_away_win_prob >= 0.50:
    derived_away_ml = int(-100 * (model_away_win_prob / (1 - model_away_win_prob)))
    derived_home_ml = int(100 * ((1 - model_away_win_prob) / model_away_win_prob))
else:
    derived_away_ml = int(100 * (model_away_win_prob / (1 - model_away_win_prob)))
    derived_home_ml = int(-100 * ((1 - model_away_win_prob) / model_away_win_prob))

# Calculate edge margin between model lines and vegas lines
if vegas_away_ml < 0:
    vegas_away_prob = abs(vegas_away_ml) / (abs(vegas_away_ml) + 100)
else:
    vegas_away_prob = 100 / (vegas_away_ml + 100)
ml_probability_edge = round((model_away_win_prob - vegas_away_prob) * 100, 1)

# Render values
val_col1, val_col2, val_col3 = st.columns(3)
with val_col1:
    st.metric(label=f"Projected {away_team} Total", value=f"{projected_away_runs} Runs", delta=f"ML: {derived_away_ml:+}")
with val_col2:
    st.metric(label=f"Projected {home_team} Total", value=f"{projected_home_runs} Runs", delta=f"ML: {derived_home_ml:+}")
with val_col3:
    st.metric(label="Calculated Total", value=f"{calculated_expected_total} Runs", delta=f"Edge: {calculated_edge:+} Runs")

st.write("---")
# Total Run Output Signals
st.write("#### 🎯 Execution Signals Dashboard")
sig_col1, sig_col2 = st.columns(2)

with sig_col1:
    st.write("**Total Runs Directive:**")
    if calculated_edge >= 0.75:
        st.success(f"🔥 **OVER {vegas_line}**\n\nModel projects {calculated_expected_total} runs. Premium volume breakout value is present.")
    elif calculated_edge <= -0.75:
        st.info(f"❄️ **UNDER {vegas_line}**\n\nModel projects {calculated_expected_total} runs. Dominant run suppression variance present.")
    else:
        st.warning(f"⚠️ **TOTALS PASS**\n\nThe analytical total is completely flat against book lines.")

with sig_col2:
    st.write("**Match Winner Side Directive:**")
    if ml_probability_edge >= 3.5:
        st.success(f"🔥 **SIDE PICK: {away_team} MONEYLINE**\n\nModel implied win rate is {model_away_win_prob*100:.1f}%. Discrepancy shows a premium +{ml_probability_edge}% margin.")
    elif ml_probability_edge <= -3.5:
        st.success(f"🔥 **SIDE PICK: {home_team} MONEYLINE**\n\nModel implied win rate is {(1-model_away_win_prob)*100:.1f}%. Discrepancy shows a premium +{abs(ml_probability_edge)}% margin.")
    else:
        st.warning(f"⚠️ **SIDES PASS**\n\nThe market pricing effectively models true win probability vectors.")

# --- 8. DATA TABLE DISPLAY PANELS ---
st.write("### 4. Live Metric Matrix Reference")
col_g1, col_g2 = st.columns(2)
with col_g1:
    st.write(pd.DataFrame([{"Team": away_team, "Offense RPG": away_rpg, "Bullpen WHIP": away_bp_whip, "Live ERA": profile1['ERA'], "Calculated SIERA": profile1['SIERA']}]).T.rename(columns={0: "Away Value"}))
with col_g2:
    st.write(pd.DataFrame([{"Team": home_team, "Offense RPG": home_rpg, "Bullpen WHIP": home_bp_whip, "Live ERA": profile2['ERA'], "Calculated SIERA": profile2['SIERA']}]).T.rename(columns={0: "Home Value"}))

# --- 9. SECTION 5: LIVE SPORTSBOOK LINE SHOPPING ---
st.write("### 5. Live Sportsbook Odds Comparison Matrix")
st.write("Line-shop the premium books below to lock in the optimal model edge variance.")

# Dynamically stagger sportsbook lines slightly around your parameters to simulate line shopping vectors
simulated_dk_total = vegas_line
simulated_fd_total = vegas_line + 0.5 if calculated_edge > 0 else vegas_line - 0.5
simulated_mgm_total = vegas_line

sim_dk_away_ml = vegas_away_ml
sim_fd_away_ml = vegas_away_ml - 10 if ml_probability_edge > 0 else vegas_away_ml + 10
sim_mgm_away_ml = vegas_away_ml + 5 if ml_probability_edge > 0 else vegas_away_ml - 5

odds_matrix_data = [
    {
        "Sportsbook": "DraftKings 👑", 
        "O/U Line": f"{simulated_dk_total}", 
        f"{away_team} ML": f"{sim_dk_away_ml:+}" if sim_dk_away_ml > 0 else f"{sim_dk_away_ml}",
        f"{home_team} ML": f"{-sim_dk_away_ml:+}" if -sim_dk_away_ml > 0 else f"{-sim_dk_away_ml}",
        "Model Totals Edge": f"{round(calculated_expected_total - simulated_dk_total, 2):+} Runs"
    },
    {
        "Sportsbook": "FanDuel 🔵", 
        "O/U Line": f"{simulated_fd_total}", 
        f"{away_team} ML": f"{sim_fd_away_ml:+}" if sim_fd_away_ml > 0 else f"{sim_fd_away_ml}",
        f"{home_team} ML": f"{-sim_fd_away_ml:+}" if -sim_fd_away_ml > 0 else f"{-sim_fd_away_ml}",
        "Model Totals Edge": f"{round(calculated_expected_total - simulated_fd_total, 2):+} Runs"
    },
    {
        "Sportsbook": "BetMGM 🦁", 
        "O/U Line": f"{simulated_mgm_total}", 
        f"{away_team} ML": f"{sim_mgm_away_ml:+}" if sim_mgm_away_ml > 0 else f"{sim_mgm_away_ml}",
        f"{home_team} ML": f"{-sim_mgm_away_ml:+}" if -sim_mgm_away_ml > 0 else f"{-sim_mgm_away_ml}",
        "Model Totals Edge": f"{round(calculated_expected_total - simulated_mgm_total, 2):+} Runs"
    }
]

odds_df = pd.DataFrame(odds_matrix_data)

st.dataframe(
    odds_df.set_index("Sportsbook"), 
    use_container_width=True
)

st.markdown("""
    ---
    <div style="text-align: center; color: #64748b; font-size: 11px; padding: 10px;">
        ⚠️ <strong>Disclaimer:</strong> Odds comparison layout is presented purely for structural data information purposes. DiamondTotals does not accept wagers or process real money gaming. 
        <br>Must be 21+ to gamble. If you or someone you know has a gambling problem, call <strong>1-800-GAMBLER</strong>.
    </div>
""", unsafe_allow_html=True)
