import streamlit as st
import random

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Visual Streamlit Ludo", page_icon="🎲", layout="centered")

st.title("🎲 Visual 4-Player Ludo Arena")
st.write("A visually mapped Ludo game running on native Streamlit layout engines.")

# --- 2. GAME SETUP & STATE MANIFESTS ---
PLAYERS = ["Red", "Green", "Yellow", "Blue"]
TRACK_LIMIT = 24  # Compact 24-step loop path layout

# Precise 2D Grid coordinates layout for a visual track arena matrix
GRID_PATH = [
    (0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0), # Top Arm Loop
    (4,0), (5,0), (5,1), (5,2), (5,3), (6,3), (7,3), # Right Arm Loop
    (7,4), (7,5), (6,5), (5,5), (5,6), (5,7), (4,7), # Bottom Arm Loop
    (3,7), (2,7), (2,6), (2,5), (1,5), (0,5), (0,4)  # Left Arm Loop
]

PLAYER_EMOJIS = {"Red": "🔴", "Green": "🟢", "Yellow": "🟡", "Blue": "🔵"}
YARD_COORDINATES = {"Red": (1, 1), "Green": (6, 1), "Yellow": (6, 6), "Blue": (1, 6)}

if "game_setup" not in st.session_state:
    st.session_state.turn_idx = 0
    st.session_state.dice_value = 1
    st.session_state.has_rolled = False
    st.session_state.logs = ["Game initialized! Red player rolls first."]
    
    # -1 means inside Yard. 0-23 means track position steps. 999 means Goal.
    st.session_state.player_positions = {
        "Red": [-1, -1],
        "Green": [-1, -1],
        "Yellow": [-1, -1],
        "Blue": [-1, -1]
    }

def add_log(text):
    st.session_state.logs.insert(0, text)

current_player = PLAYERS[st.session_state.turn_idx]

# --- 3. CORE LOGIC OPERATIONS ---
def roll_dice():
    st.session_state.dice_value = random.randint(1, 6)
    st.session_state.has_rolled = True
    add_log(f"🎲 {current_player} rolled a {st.session_state.dice_value}!")
    
    tokens = st.session_state.player_positions[current_player]
    if all(pos == -1 for pos in tokens) and st.session_state.dice_value != 6:
        add_log(f"➔ {current_player} has no valid moves available. Passing turn.")
        pass_turn()

def pass_turn():
    st.session_state.turn_idx = (st.session_state.turn_idx + 1) % 4
    st.session_state.has_rolled = False

def move_token(token_index):
    dice = st.session_state.dice_value
    positions = st.session_state.player_positions[current_player]
    current_pos = positions[token_index]
    
    if current_pos == -1:
        if dice == 6:
            positions[token_index] = 0
            add_log(f"🚀 {current_player} deployed Token {token_index + 1} onto the track!")
        else:
            return
    else:
        new_pos = current_pos + dice
        if new_pos >= TRACK_LIMIT:
            positions[token_index] = 999
            add_log(f"🏆 {current_player} Token {token_index + 1} reached the central Goal!")
        else:
            positions[token_index] = new_pos
            add_log(f"🏃 {current_player} moved Token {token_index + 1} to track position {new_pos}.")
            
            # Catch collision processing
            for opponent in PLAYERS:
                if opponent != current_player:
                    opp_positions = st.session_state.player_positions[opponent]
                    for idx, opp_pos in enumerate(opp_positions):
                        if opp_pos == new_pos and opp_pos != -1 and opp_pos != 999:
                            opp_positions[idx] = -1
                            add_log(f"💥 {current_player} sent {opponent}'s Token {idx + 1} back to Yard!")

    pass_turn()

# --- 4. GRAPHIC MATRIX RENDERING SYSTEM ---
# Construct an empty 8x8 matrix board grid area layout
matrix = [["⬜" for _ in range(8)] for _ in range(8)]

# Fill central base goal point
matrix[4][4] = "👑"

# Label track paths with empty dot tracks
for (x, y) in GRID_PATH:
    matrix[y][x] = "⚫"

# Pin Home Base Yard Zones onto map matrix fields
for name, (yx, yy) in YARD_COORDINATES.items():
    matrix[yy][yx] = PLAYER_EMOJIS[name]

# Map Active Tokens coordinates onto the grid system layout interface
for p_name in PLAYERS:
    emoji = PLAYER_EMOJIS[p_name]
    for pos in st.session_state.player_positions[p_name]:
        if pos != -1 and pos != 999:
            # Map index positions loop array coordinates safely
            tx, ty = GRID_PATH[pos % TRACK_LIMIT]
            matrix[ty][tx] = emoji

# --- 5. STREAMLIT UI UX RENDERING FRAMEWORK ---
col_map, col_controls = st.columns([1.2, 1])

with col_map:
    st.subheader("🗺️ Live Arena Map Grid")
    # Output the matrix grid inside a clean scannable text box format
    board_output = ""
    for row in matrix:
        board_output += " ".join(row) + "\n"
    st.code(board_output, language="text")

with col_controls:
    st.subheader(f"🎯 Turn: {PLAYER_EMOJIS[current_player]} {current_player}")
    
    if not st.session_state.has_rolled:
        st.button("Roll Dice 🎲", on_click=roll_dice, use_container_width=True)
    else:
        st.metric(label="Dice Result", value=f"🎲 {st.session_state.dice_value}")
        tokens = st.session_state.player_positions[current_player]
        
        for i in range(2):
            pos = tokens[i]
            if pos == -1:
                lbl = f"Deploy Token {i+1} (Needs a 6)"
                can_move = (st.session_state.dice_value == 6)
            elif pos == 999:
                lbl = f"Token {i+1}: Finished 🏆"
                can_move = False
            else:
                lbl = f"Advance Token {i+1} (Pos: {pos})"
                can_move = True
                
            st.button(lbl, disabled=not can_move, key=f"t_{i}", on_click=move_token, args=(i,), use_container_width=True)
            
        st.button("Skip Turn ➔", on_click=pass_turn, use_container_width=True)

st.markdown("---")
st.subheader("📋 Match Broadcast Logs")
st.caption("Tracking last 4 live combat updates:")
for log in st.session_state.logs[:4]:
    st.write(log)
