import streamlit as st
import random

# -----------------------------------------------------------------------------
# 1. PREMIUM LUDO KING HIGH-UX STYLING (CSS Injection)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Ludo King Elite Arena",
    page_icon="🎲",
    layout="wide"
)

# Custom injection for sleek arcade styling, player halos, and retro font highlights
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    .stApp {
        background: radial-gradient(circle, #1a1c29 0%, #0e1017 100%);
        color: #FFFFFF;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Premium Arcade Header Styling */
    .ludo-header {
        text-align: center;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0px;
        text-shadow: 0px 4px 10px rgba(255, 215, 0, 0.2);
    }
    
    /* Control Box Styling */
    .control-box {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Active player glowing panel */
    .active-halo {
        animation: pulse-border 1.5s infinite alternate;
    }
    @keyframes pulse-border {
        0% { box-shadow: 0 0 5px #FFD700, inset 0 0 5px #FFD700; }
        100% { box-shadow: 0 0 20px #FFD700, inset 0 0 10px #FFD700; }
    }
    
    /* Native button styling overrides to match Ludo King theme */
    div.stButton > button {
        background: linear-gradient(135deg, #FF1493 0%, #C71585 100%);
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        box-shadow: 0 4px 15px rgba(255, 20, 147, 0.4) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 20, 147, 0.6) !important;
    }
    div.stButton > button:disabled {
        background: #3a3b45 !important;
        box-shadow: none !important;
        color: #888888 !important;
        transform: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. STATE LOGIC ENGINE (4 Players, 2 Pawns Each)
# -----------------------------------------------------------------------------
PLAYERS = ["Red", "Green", "Yellow", "Blue"]
COLORS = {
    "Red": "#FF3366",
    "Green": "#2ECC71",
    "Yellow": "#F1C40F",
    "Blue": "#3498DB"
}
LIGHT_COLORS = {
    "Red": "#FF99B2",
    "Green": "#A3E4D7",
    "Yellow": "#F9E79F",
    "Blue": "#AED6F1"
}

# The classic cross-track layout coordinates (15x15 Ludo structural grid)
BOARD_PATH = [
    (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (6,5), (6,4), (6,3), (6,2), (6,1), (6,0), # Top-Left to Top
    (7,0), (8,0), (8,1), (8,2), (8,3), (8,4), (8,5), (9,6), (10,6), (11,6), (12,6), (13,6), (14,6), # Top-Right to Right
    (14,7), (14,8), (13,8), (12,8), (11,8), (10,8), (9,8), (8,9), (8,10), (8,11), (8,12), (8,13), (8,14), # Bottom-Right to Bottom
    (7,14), (6,14), (6,13), (6,12), (6,11), (6,10), (6,9), (5,8), (4,8), (3,8), (2,8), (1,8), (0,8), (0,7)  # Bottom-Left to Left
]
TRACK_LEN = len(BOARD_PATH)

# Ludo King standard entry block indices on the track array
START_OFFSETS = {"Red": 0, "Green": 13, "Yellow": 26, "Blue": 39}

# Ludo King traditional star/safety tiles mapping
SAFETY_TILES = [0, 8, 13, 21, 26, 34, 39, 47]

if "ludo_king_state" not in st.session_state:
    st.session_state.ludo_king_state = True
    st.session_state.turn_idx = 0
    st.session_state.dice_val = 6
    st.session_state.has_rolled = False
    st.session_state.winner = None
    st.session_state.match_logs = ["🏰 Arena ready! Red rolls first."]
    
    # Position tracking: -1 = Base, 0-50 = Steps along track, 51+ = Home Triangle Stretch, 999 = Done
    st.session_state.pawns = {
        "Red": [-1, -1],
        "Green": [-1, -1],
        "Yellow": [-1, -1],
        "Blue": [-1, -1]
    }

def post_log(text):
    st.session_state.match_logs.insert(0, text)

active_p = PLAYERS[st.session_state.turn_idx]

# -----------------------------------------------------------------------------
# 3. INTERACTIVE MOVEMENT FUNCTIONS
# -----------------------------------------------------------------------------
def trigger_roll():
    st.session_state.dice_val = random.randint(1, 6)
    st.session_state.has_rolled = True
    post_log(f"🎲 **{active_p}** rolled a gorgeous **{st.session_state.dice_val}**!")
    
    # Auto-pass rule if all pawns are locked and roll is not a 6
    player_pawns = st.session_state.pawns[active_p]
    if all(pos == -1 for pos in player_pawns) and st.session_state.dice_val != 6:
        post_log(f"➔ {active_p} holds no escape moves. Passing dice.")
        forward_turn()

def forward_turn():
    st.session_state.turn_idx = (st.session_state.turn_idx + 1) % 4
    st.session_state.has_rolled = False

def execution_move(pawn_index):
    roll = st.session_state.dice_val
    positions = st.session_state.pawns[active_p]
    current_pos = positions[pawn_index]
    
    if current_pos == -1:
        if roll == 6:
            positions[pawn_index] = 0
            post_log(f"🚀 {active_p} Pawn {pawn_index + 1} escaped onto starting grid!")
            # Retain turn on rolling a 6 just like Ludo King!
            st.session_state.has_rolled = False
            return
    else:
        target_pos = current_pos + roll
        if target_pos >= 51:
            positions[pawn_index] = 999
            post_log(f"👑 {active_p} Pawn {pawn_index + 1} finished and entered the Home base!")
        else:
            positions[pawn_index] = target_pos
            post_log(f"🏃 {active_p} Pawn {pawn_index + 1} advanced {roll} tiles.")
            check_board_captures(active_p, pawn_index, target_pos)
            
    forward_turn()

def check_board_captures(current_player, p_idx, relative_pos):
    # Map back to global track index array to find overlap conflicts
    start_offset = START_OFFSETS[current_player]
    global_active_idx = (relative_pos + start_offset) % TRACK_LEN
    
    # Safety rule verification
    if global_active_idx in SAFETY_TILES:
        return
        
    for opponent in PLAYERS:
        if opponent == current_player:
            continue
        opp_offset = START_OFFSETS[opponent]
        for opp_p_idx, opp_pos in enumerate(st.session_state.pawns[opponent]):
            if opp_pos != -1 and opp_pos != 999 and opp_pos < 45:
                global_opp_idx = (opp_pos + opp_offset) % TRACK_LEN
                if global_active_idx == global_opp_idx:
                    st.session_state.pawns[opponent][opp_p_idx] = -1
                    post_log(f"💥 EXPLOSION! {current_player} captured {opponent}'s Pawn {opp_p_idx+1}!")

# -----------------------------------------------------------------------------
# 4. HIGH-UX VECTOR CANVAS GENERATION (SVG Rendering)
# -----------------------------------------------------------------------------
def build_premium_ludo_svg():
    dim = 600
    tile = dim / 15
    p_radius = tile * 0.38
    
    svg = f'<svg width="100%" height="{dim}" viewBox="0 0 {dim} {dim}" style="background-color:#1e2130; border-radius:20px; box-shadow: 0px 12px 40px rgba(0,0,0,0.6); border: 3px solid rgba(255,255,255,0.1);">'
    
    # Custom Gradient Filters for Ludo King aesthetic glow effects
    svg += """
    <defs>
        <radialGradient id="redG" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FF6699"/><stop offset="100%" stop-color="#CC0033"/></radialGradient>
        <radialGradient id="greenG" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#66FF99"/><stop offset="100%" stop-color="#009933"/></radialGradient>
        <radialGradient id="yellowG" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FFFFCC"/><stop offset="100%" stop-color="#D4AC0D"/></radialGradient>
        <radialGradient id="blueG" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#66CCFF"/><stop offset="100%" stop-color="#1F618D"/></radialGradient>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="3" flood-opacity="0.5"/></filter>
    </defs>
    """
    
    # 1. Standard Quad Quadrants Base Squares
    svg += f'<rect x="0" y="0" width="{tile*6}" height="{tile*6}" fill="url(#redG)" rx="8"/>'
    svg += f'<rect x="{tile*9}" y="0" width="{tile*6}" height="{tile*6}" fill="url(#greenG)" rx="8"/>'
    svg += f'<rect x="{tile*9}" y="{tile*9}" width="{tile*6}" height="{tile*6}" fill="url(#yellowG)" rx="8"/>'
    svg += f'<rect x="0" y="{tile*9}" width="{tile*6}" height="{tile*6}" fill="url(#blueG)" rx="8"/>'
    
    # Home Yard Internal White Tokens Platform Circles
    yards = {"red": (tile*3, tile*3), "green": (tile*12, tile*3), "yellow": (tile*12, tile*12), "blue": (tile*3, tile*12)}
    for key, (cx, cy) in yards.items():
        svg += f'<circle cx="{cx}" cy="{cy}" r="{tile*2.2}" fill="#ffffff" opacity="0.2"/>'

    # 2. Track Grid Cells & Safety Zones Map Painting Loops
    for i in range(15):
        for j in range(15):
            if (6 <= i <= 8) or (6 <= j <= 8):
                if 6 <= i <= 8 and 6 <= j <= 8:
                    continue # Skip central triangle space
                cx, cy = i * tile, j * tile
                
                # Base track structural fill color layouts
                f_color = "#2c2f44"
                
