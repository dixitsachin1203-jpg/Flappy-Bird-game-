import streamlit as st
import random

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & STRUCTURAL THEME DESIGN
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Neon Ludo Arena",
    page_icon="🎲",
    layout="wide"
)

# Custom high-end dark UI style modifications
st.markdown("""
    <style>
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
    }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FF0055 0%, #7A00FF 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(122, 0, 255, 0.4);
    }
    .player-card {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #1E293B;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. GAME STATE MANAGEMENT (Core Game Loop Engine)
# -----------------------------------------------------------------------------
# Define players, positions on board tracks, and color tokens
PLAYERS = ["Red", "Green", "Yellow", "Blue"]
PLAYER_COLORS = {
    "Red": "#FF2E63",
    "Green": "#08D9D6",
    "Yellow": "#F9ED69",
    "Blue": "#252A34"
}
HEX_COLORS = {"Red": "#FF2E63", "Green": "#00F5D4", "Yellow": "#FFEE32", "Blue": "#00B4D8"}

# Track paths mapping positions (0 to 40)
# Simple track logic mapping for a basic 40-step visual circle loop
BOARD_PATH = [
    (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (6,5), (6,4), (6,3), (6,2), (6,1), (6,0),
    (7,0), (8,0), (8,1), (8,2), (8,3), (8,4), (8,5), (9,6), (10,6), (11,6), (12,6), (13,6), (14,6),
    (14,7), (14,8), (13,8), (12,8), (11,8), (10,8), (9,8), (8,9), (8,10), (8,11), (8,12), (8,13), (8,14),
    (7,14), (6,14), (6,13), (6,12), (6,11), (6,10), (6,9), (5,8), (4,8), (3,8), (2,8), (1,8), (0,8), (0,7)
]
TRACK_LEN = len(BOARD_PATH)

# Initialize persistent session tracking structures
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.turn_idx = 0
    st.session_state.dice_value = 1
    st.session_state.has_rolled = False
    st.session_state.game_log = ["Welcome to Neon Ludo Arena! Roll dice to begin."]
    
    # 4 Players, each has 2 active game tokens/pieces
    # Value is progress steps along their path. -1 means locked at Home Base.
    st.session_state.pieces = {
        "Red": [ -1, -1 ],
        "Green": [ -1, -1 ],
        "Yellow": [ -1, -1 ],
        "Blue": [ -1, -1 ]
    }

def log_event(message):
    st.session_state.game_log.insert(0, message)
    if len(st.session_state.game_log) > 6:
        st.session_state.game_log.pop()

current_player = PLAYERS[st.session_state.turn_idx]

# -----------------------------------------------------------------------------
# 3. ACTION HANDLERS
# -----------------------------------------------------------------------------
def roll_dice():
    st.session_state.dice_value = random.randint(1, 6)
    st.session_state.has_rolled = True
    log_event(f"🎲 {current_player} rolled a **{st.session_state.dice_value}**!")
    
    # Validation check: If player has all tokens in home yard and didn't roll a 6, skip turn automatically
    tokens = st.session_state.pieces[current_player]
    if all(p == -1 for p in tokens) and st.session_state.dice_value != 6:
        log_event(f"➔ No valid moves for {current_player}. Passing turn.")
        pass_turn()

def pass_turn():
    st.session_state.turn_idx = (st.session_state.turn_idx + 1) % 4
    st.session_state.has_rolled = False

def move_piece(piece_index):
    dice = st.session_state.dice_value
    tokens = st.session_state.pieces[current_player]
    current_pos = tokens[piece_index]
    
    if current_pos == -1:
        if dice == 6:
            tokens[piece_index] = 0  # Deploy token to starting position block
            log_event(f"🚀 {current_player} deployed Piece {piece_index + 1} from Yard!")
        else:
            return  # Can't move locked token without a 6
    else:
        new_pos = current_pos + dice
        if new_pos >= TRACK_LEN:
            log_event(f"🏆 {current_player} Piece {piece_index + 1} reached Goal!")
            tokens[piece_index] = 999  # Completed track state value
        else:
            tokens[piece_index] = new_pos
            log_event(f"🏃 {current_player} moved Piece {piece_index + 1} forward {dice} steps.")
            
            # Simple collision capture algorithm check
            check_collisions(current_player, piece_index, new_pos)
            
    pass_turn()

def check_collisions(active_player, active_idx, target_pos):
    # Standard absolute offset for matching board loops accurately
    player_start_offsets = {"Red": 0, "Green": 13, "Yellow": 26, "Blue": 38}
    act_off = player_start_offsets[active_player]
    abs_active_grid_idx = (target_pos + act_off) % TRACK_LEN
    
    for opp in PLAYERS:
        if opp == active_player:
            continue
        opp_off = player_start_offsets[opp]
        for idx, pos in enumerate(st.session_state.pieces[opp]):
            if pos != -1 and pos != 999:
                abs_opp_grid_idx = (pos + opp_off) % TRACK_LEN
                if abs_active_grid_idx == abs_opp_grid_idx:
                    st.session_state.pieces[opp][idx] = -1  # Send back to yard
                    log_event(f"💥 {active_player} captured {opp}'s Piece {idx + 1} back to base!")

# -----------------------------------------------------------------------------
# 4. RENDERING HIGH-UX CANVAS VECTOR LAYOUTS
# -----------------------------------------------------------------------------
def generate_board_svg():
    # Draw precise vector blocks for crisp resolution across displays
    svg_size = 500
    cell_size = svg_size / 15
    
    svg = f'<svg width="100%" height="{svg_size}" viewBox="0 0 {svg_size} {svg_size}" style="background-color:#151D30; border-radius:12px; box-shadow: 0px 4px 20px rgba(0,0,0,0.5);">'
    
    # 1. Structural Quad Background Fills
    svg += f'<rect x="0" y="0" width="{cell_size*6}" height="{cell_size*6}" fill="#FF2E63" opacity="0.15"/>'
    svg += f'<rect x="{cell_size*9}" y="0" width="{cell_size*6}" height="{cell_size*6}" fill="#00F5D4" opacity="0.15"/>'
    svg += f'<rect x="0" y="{cell_size*9}" width="{cell_size*6}" height="{cell_size*6}" fill="#00B4D8" opacity="0.15"/>'
    svg += f'<rect x="{cell_size*9}" y="{cell_size*9}" width="{cell_size*6}" height="{cell_size*6}" fill="#FFEE32" opacity="0.15"/>'
    
    # 2. Central Victory Matrix Cross Hub
    svg += f'<polygon points="{cell_size*6},{cell_size*6} {cell_size*9},{cell_size*6} {cell_size*7.5},{cell_size*7.5}" fill="#00F5D4" opacity="0.4"/>'
    svg += f'<polygon points="{cell_size*9},{cell_size*6} {cell_size*9},{cell_size*9} {cell_size*7.5},{cell_size*7.5}" fill="#FFEE32" opacity="0.4"/>'
    svg += f'<polygon points="{cell_size*6},{cell_size*9} {cell_size*9},{cell_size*9} {cell_size*7.5},{cell_size*7.5}" fill="#00B4D8" opacity="0.4"/>'
    svg += f'<polygon points="{cell_size*6},{cell_size*6} {cell_size*6},{cell_size*9} {cell_size*7.5},{cell_size*7.5}" fill="#FF2E63" opacity="0.4"/>'

    # 3. Draw Track Grid Outlines
    for x in range(15):
        for y in range(15):
            # Exclude home fields and center matrix from raw block grids
            if (6 <= x <= 8) or (6 <= y <= 8):
                if not (6 <= x <= 8 and 6 <= y <= 8):
                    cx = x * cell_size
                    cy = y * cell_size
                    svg += f'<rect x="{cx}" y="{cy}" width="{cell_size}" height="{cell_size}" fill="none" stroke="#2D3748" stroke-width="1"/>'

    # 4. Plot Active Tokens onto Track
    player_start_offsets = {"Red": 0, "Green": 13, "Yellow": 26, "Blue": 38}
    
    # Specific coordinates for home yards so they display clearly when locked
    home_coordinates = {
        "Red": [(1.5, 1.5), (3.5, 3.5)],
        "Green": [(11.5, 1.5), (13.5, 3.5)],
        "Yellow": [(11.5, 11.5), (13.5, 13.5)],
        "Blue": [(1.5, 11.5), (3.5, 13.5)]
    }

    for p_name in PLAYERS:
        color = HEX_COLORS[p_name]
        offset = player_start_offsets[p_name]
        for idx, pos in enumerate(st.session_state.pieces[p_name]):
            if pos == -1: # Safe Home Base display coordinates
                hx, hy = home_coordinates[p_name][idx]
                cx, cy = hx * cell_size, hy * cell_size
            elif pos == 999: # Goal state node placement coordinates
                cx, cy = 7.5 * cell_size, 7.5 * cell_size
            else:
                grid_idx = (pos + offset) % TRACK_LEN
                bx, by = BOARD_PATH[grid_idx]
                cx, cy = (bx + 0.5) * cell_size, (by + 0.5) * cell_size
                
            # SVG Circle Token Drawing Markup
            svg += f'<circle cx="{cx}" cy="{cy}" r="{cell_size*0.35}" fill="{color}" stroke="#FFFFFF" stroke-width="2" shadow="0 2px 5px rgba(0,0,0,0.5)"/>'
            svg += f'<text x="{cx}" y="{cy+4}" font-size="12" font-weight="bold" fill="#000" text-anchor="middle">{idx+1}</text>'
            
    svg += '</svg>'
    return svg

# -----------------------------------------------------------------------------
# 5. DASHBOARD LAYOUT DRAWING IMPLEMENTATION
# -----------------------------------------------------------------------------
st.title("🎲 Arena Ludo Multi-Engine")
st.caption("A premium HTML5 Canvas game dashboard executing local multiplayer loops.")

col1, col2 = st.columns([3, 2])

with col1:
    # Build Interactive Custom Graphics Framework Board Frame
    board_html = generate_board_svg()
    st.markdown(board_html, unsafe_allow_html=True)

with col2:
    # System Command Control Panel Interface Console
