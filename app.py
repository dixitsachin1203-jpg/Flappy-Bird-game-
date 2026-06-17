import streamlit as st
import random

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Simple Streamlit Ludo", page_icon="🎲")

st.title("🎲 Simple 4-Player Ludo")
st.write("A clean, text-based Ludo game using reliable native Streamlit buttons.")

# --- 2. GAME STATE INITIALIZATION ---
# 4 Players, each has 2 tokens
PLAYERS = ["Red", "Green", "Yellow", "Blue"]
TRACK_LIMIT = 40  # Simple linear track length for safety

if "game_setup" not in st.session_state:
    st.session_state.game_setup = True
    st.session_state.turn_idx = 0
    st.session_state.dice_value = 1
    st.session_state.has_rolled = False
    st.session_state.logs = ["Game started! Red plays first."]
    
    # -1 means inside Yard. 0-40 means track position. 999 means Finished.
    st.session_state.player_positions = {
        "Red": [-1, -1],
        "Green": [-1, -1],
        "Yellow": [-1, -1],
        "Blue": [-1, -1]
    }

# Helper to log events easily
def add_log(text):
    st.session_state.logs.insert(0, text)

current_player = PLAYERS[st.session_state.turn_idx]

# --- 3. GAME ACTIONS ---
def roll_dice():
    st.session_state.dice_value = random.randint(1, 6)
    st.session_state.has_rolled = True
    add_log(f"🎲 {current_player} rolled a {st.session_state.dice_value}!")
    
    # Auto-skip check: if stuck in yard and didn't roll a 6
    tokens = st.session_state.player_positions[current_player]
    if all(pos == -1 for pos in tokens) and st.session_state.dice_value != 6:
        add_log(f"➔ {current_player} has no valid moves. Passing turn.")
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
            add_log(f"🚀 {current_player} moved Token {token_index + 1} onto the track!")
        else:
            return  # Safety fallback
    else:
        new_pos = current_pos + dice
        if new_pos >= TRACK_LIMIT:
            positions[token_index] = 999
            add_log(f"🏆 {current_player} Token {token_index + 1} reached the Goal!")
        else:
            positions[token_index] = new_pos
            add_log(f"🏃 {current_player} moved Token {token_index + 1} to position {new_pos}.")
            
            # Simple landing collision mechanic
            for opponent in PLAYERS:
                if opponent != current_player:
                    opp_positions = st.session_state.player_positions[opponent]
                    for idx, opp_pos in enumerate(opp_positions):
                        if opp_pos == new_pos and opp_pos != -1 and opp_pos != 999:
                            opp_positions[idx] = -1
                            add_log(f"💥 {current_player} sent {opponent}'s Token {idx + 1} back to base!")

    pass_turn()

# --- 4. STREAMLIT INTERFACE ---

# Sidebar: Live Game Logs
st.sidebar.header("📋 Game Match Logs")
for log in st.session_state.logs[:10]:  # Show last 10 entries
    st.sidebar.write(log)

# Main Panel: Current Status Dashboard
col1, col2 = st.columns(2)
with col1:
    st.subheader("🎯 Active Player")
    st.subheader(f"👉 **{current_player}**")

with col2:
    st.subheader("🎲 Current Dice")
    st.metric(label="Dice Roll Result", value=st.session_state.dice_value)

st.markdown("---")

# Controls Section
st.subheader("🕹️ Controls")
if not st.session_state.has_rolled:
    st.button("Roll Dice 🎲", on_click=roll_dice, use_container_width=True)
else:
    st.write("Choose a valid token action below:")
    tokens = st.session_state.player_positions[current_player]
    
    c1, c2 = st.columns(2)
    for i in range(2):
        pos = tokens[i]
        
        # Display state descriptions
        if pos == -1:
            lbl = f"Token {i+1}: Locked in Home Base"
            # Can only move from base if rolled a 6
            can_move = (st.session_state.dice_value == 6)
        elif pos == 999:
            lbl = f"Token {i+1}: Finished 🏆"
            can_move = False
        else:
            lbl = f"Token {i+1}: At Position {pos}"
            can_move = True
            
        with (c1 if i == 0 else c2):
            st.button(lbl, disabled=not can_move, on_click=move_token, args=(i,), use_container_width=True)
            
    st.button("Skip / Pass Turn ➔", on_click=pass_turn, use_container_width=True)

st.markdown("---")

# Board Status Table (Clean Native Metrics Grid)
st.subheader("📊 Board Leaderboard Positions")
grid_cols = st.columns(4)

for index, p_name in enumerate(PLAYERS):
    with grid_cols[index]:
        st.markdown(f"### {p_name}")
        p_tokens = st.session_state.player_positions[p_name]
        
        for t_idx, pos in enumerate(p_tokens):
            if pos == -1:
                display_status = "🏠 Home Yard"
            elif pos == 999:
                display_status = "🏁 Finished!"
            else:
                display_status = f"📍 Step {pos}"
                
            st.write(f"**Token {t_idx+1}:** {display_status}")

# System Reset
if st.sidebar.button("🔄 Reset Whole Game"):
    st.session_state.clear()
    st.rerun()
