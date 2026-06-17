import streamlit as st
import random

st.set_page_config(
    page_title="🎲 Ludo Royale",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------

st.markdown("""
<style>

.main{
    background:#f4f7fb;
}

.title{
    text-align:center;
    font-size:50px;
    font-weight:bold;
    color:#ff4b4b;
}

.player-card{
    padding:15px;
    border-radius:15px;
    color:white;
    font-weight:bold;
    text-align:center;
}

.red{
    background:#ff4b4b;
}

.green{
    background:#1abc9c;
}

.yellow{
    background:#f1c40f;
    color:black;
}

.blue{
    background:#3498db;
}

.dice{
    text-align:center;
    font-size:120px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🎲 Ludo Royale</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Initialize Game
# -----------------------------

if "positions" not in st.session_state:

    st.session_state.positions = {
        "Red":[0,0,0,0],
        "Green":[0,0,0,0],
        "Yellow":[0,0,0,0],
        "Blue":[0,0,0,0]
    }

if "turn" not in st.session_state:
    st.session_state.turn = 0

players = ["Red","Green","Yellow","Blue"]

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("Game Status")

current_player = players[st.session_state.turn]

st.sidebar.success(
    f"Current Turn : {current_player}"
)

# -----------------------------
# Player Cards
# -----------------------------

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown(
        '<div class="player-card red">RED</div>',
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        '<div class="player-card green">GREEN</div>',
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        '<div class="player-card yellow">YELLOW</div>',
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        '<div class="player-card blue">BLUE</div>',
        unsafe_allow_html=True
    )

st.divider()

# -----------------------------
# Dice
# -----------------------------

dice_faces = {
    1:"⚀",
    2:"⚁",
    3:"⚂",
    4:"⚃",
    5:"⚄",
    6:"⚅"
}

if "dice" not in st.session_state:
    st.session_state.dice = 1

col1,col2,col3 = st.columns([1,2,1])

with col2:

    st.markdown(
        f"<div class='dice'>{dice_faces[st.session_state.dice]}</div>",
        unsafe_allow_html=True
    )

    if st.button("🎲 Roll Dice", use_container_width=True):

        roll = random.randint(1,6)

        st.session_state.dice = roll

        st.success(
            f"{current_player} rolled {roll}"
        )

# -----------------------------
# Tokens
# -----------------------------

st.subheader("Player Tokens")

for player in players:

    st.write(f"### {player}")

    cols = st.columns(4)

    for i in range(4):

        with cols[i]:

            pos = st.session_state.positions[player][i]

            st.metric(
                f"Token {i+1}",
                pos
            )

            if player == current_player:

                if st.button(
                    f"Move {player}-{i+1}",
                    key=f"{player}_{i}"
                ):

                    st.session_state.positions[player][i] += st.session_state.dice

                    if st.session_state.positions[player][i] > 57:
                        st.session_state.positions[player][i] = 57

                    st.session_state.turn = (
                        st.session_state.turn + 1
                    ) % 4

                    st.rerun()

# -----------------------------
# Winner
# -----------------------------

for player in players:

    if all(
        token == 57
        for token in st.session_state.positions[player]
    ):

        st.balloons()

        st.success(
            f"🏆 {player} Wins!"
        )
