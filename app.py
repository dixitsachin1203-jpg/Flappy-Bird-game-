import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(
    page_title="🎲 Ludo Royale",
    layout="wide"
)

# ====================================
# SESSION STATE
# ====================================

if "dice" not in st.session_state:
    st.session_state.dice = 1

if "turn" not in st.session_state:
    st.session_state.turn = 0

if "tokens" not in st.session_state:

    st.session_state.tokens = {
        "red":[-1,-1,-1,-1],
        "green":[-1,-1,-1,-1],
        "yellow":[-1,-1,-1,-1],
        "blue":[-1,-1,-1,-1]
    }

players = [
    "red",
    "green",
    "yellow",
    "blue"
]

# ====================================
# LUDO PATH
# ====================================

PATH = [
(6,1),(6,2),(6,3),(6,4),(6,5),
(5,6),(4,6),(3,6),(2,6),(1,6),(0,6),
(0,7),
(0,8),
(1,8),(2,8),(3,8),(4,8),(5,8),
(6,9),(6,10),(6,11),(6,12),(6,13),(6,14),
(7,14),
(8,14),
(8,13),(8,12),(8,11),(8,10),(8,9),
(9,8),(10,8),(11,8),(12,8),(13,8),(14,8),
(14,7),
(14,6),
(13,6),(12,6),(11,6),(10,6),(9,6),
(8,5),(8,4),(8,3),(8,2),(8,1),(8,0),
(7,0)
]

# ====================================
# SAFE CELLS
# ====================================

SAFE = [0,8,13,21,26,34,39,47]

# ====================================
# HOME PATHS
# ====================================

HOME_PATHS = {

    "red":[
        (7,1),(7,2),(7,3),
        (7,4),(7,5),(7,6)
    ],

    "green":[
        (1,7),(2,7),(3,7),
        (4,7),(5,7),(6,7)
    ],

    "yellow":[
        (13,7),(12,7),(11,7),
        (10,7),(9,7),(8,7)
    ],

    "blue":[
        (7,13),(7,12),(7,11),
        (7,10),(7,9),(7,8)
    ]
}

# ====================================
# START INDEX
# ====================================

START_INDEX = {
    "red":0,
    "green":13,
    "yellow":26,
    "blue":39
}

# ====================================
# TOKEN MOVEMENT
# ====================================

def move_token(color, token_idx):

    dice = st.session_state.dice

    pos = st.session_state.tokens[color][token_idx]

    # token inside home
    if pos == -1:

        if dice == 6:
            st.session_state.tokens[color][token_idx] = 0

        return

    # move token
    pos += dice

    if pos <= 57:
        st.session_state.tokens[color][token_idx] = pos

# ====================================
# TOKEN DRAWER
# ====================================

def draw_token(svg, x, y, color):

    cell = 40

    svg += f"""
    <circle
        cx="{x*cell+20}"
        cy="{y*cell+20}"
        r="14"
        fill="{color}"
        stroke="black"
        stroke-width="2"
    />
    """

    return svg

# ====================================
# SVG START
# ====================================

cell = 40
size = 15 * cell

svg = f"""
<svg width="{size}" height="{size}"
viewBox="0 0 {size} {size}">
"""

# background

svg += f"""
<rect
width="{size}"
height="{size}"
fill="white"/>
"""

# grid

for r in range(15):

    for c in range(15):

        color = "#ffffff"

        if r < 6 and c < 6:
            color = "#ef5350"

        elif r < 6 and c > 8:
            color = "#4caf50"

        elif r > 8 and c < 6:
            color = "#fdd835"

        elif r > 8 and c > 8:
            color = "#42a5f5"

        svg += f"""
        <rect
            x="{c*cell}"
            y="{r*cell}"
            width="{cell}"
            height="{cell}"
            fill="{color}"
            stroke="black"
            stroke-width="1"
        />
        """# ====================================
# WHITE HOME BOXES
# ====================================

home_boxes = [
    (1.5,1.5),
    (9.5,1.5),
    (1.5,9.5),
    (9.5,9.5)
]

for x,y in home_boxes:

    svg += f"""
    <rect
        x="{x*cell}"
        y="{y*cell}"
        width="{3*cell}"
        height="{3*cell}"
        rx="10"
        fill="white"
        stroke="black"
        stroke-width="2"
    />
    """

# ====================================
# CENTER TRIANGLE
# ====================================

svg += f"""

<polygon
points="
300,240
360,300
300,360
240,300"
fill="white"
stroke="black"
stroke-width="2"
/>

<polygon
points="300,240 300,300 360,300"
fill="#ef5350"
/>

<polygon
points="360,300 300,300 300,360"
fill="#4caf50"
/>

<polygon
points="300,360 300,300 240,300"
fill="#42a5f5"
/>

<polygon
points="240,300 300,300 300,240"
fill="#fdd835"
/>

"""

# ====================================
# RED HOME LANE
# ====================================

for r in range(1,7):

    svg += f"""
    <rect
        x="{6*cell}"
        y="{r*cell}"
        width="{cell}"
        height="{cell}"
        fill="#ef5350"
        stroke="black"
    />
    """

# ====================================
# GREEN HOME LANE
# ====================================

for c in range(8,14):

    svg += f"""
    <rect
        x="{c*cell}"
        y="{6*cell}"
        width="{cell}"
        height="{cell}"
        fill="#4caf50"
        stroke="black"
    />
    """

# ====================================
# YELLOW HOME LANE
# ====================================

for c in range(1,7):

    svg += f"""
    <rect
        x="{c*cell}"
        y="{8*cell}"
        width="{cell}"
        height="{cell}"
        fill="#fdd835"
        stroke="black"
    />
    """

# ====================================
# BLUE HOME LANE
# ====================================

for r in range(8,14):

    svg += f"""
    <rect
        x="{8*cell}"
        y="{r*cell}"
        width="{cell}"
        height="{cell}"
        fill="#42a5f5"
        stroke="black"
    />
    """

# ====================================
# SAFE STARS
# ====================================

for pos in SAFE:

    x,y = PATH[pos]

    svg += f"""
    <text
        x="{x*cell+10}"
        y="{y*cell+30}"
        font-size="22"
        fill="black">
        ★
    </text>
    """

# ====================================
# HOME TOKENS
# ====================================

HOME_POSITIONS = {

    "red":[
        (2,2),(4,2),
        (2,4),(4,4)
    ],

    "green":[
        (10,2),(12,2),
        (10,4),(12,4)
    ],

    "yellow":[
        (2,10),(4,10),
        (2,12),(4,12)
    ],

    "blue":[
        (10,10),(12,10),
        (10,12),(12,12)
    ]
}

# ====================================
# DRAW TOKENS
# ====================================

for color in players:

    for idx,token_pos in enumerate(
        st.session_state.tokens[color]
    ):

        # token inside home

        if token_pos == -1:

            x,y = HOME_POSITIONS[color][idx]

            svg = draw_token(
                svg,
                x,
                y,
                color
            )

        # token on path

        elif token_pos < len(PATH):

            start = START_INDEX[color]

            board_pos = (
                start + token_pos
            ) % len(PATH)

            x,y = PATH[board_pos]

            svg = draw_token(
                svg,
                x,
                y,
                color
            )

# ====================================
# CLOSE SVG
# ====================================

svg += "</svg>"

# ====================================
# PAGE TITLE
# ====================================

st.markdown(
    """
    <h1 style='text-align:center'>
    🎲 Ludo Royale
    </h1>
    """,
    unsafe_allow_html=True
)

# ====================================
# BOARD DISPLAY
# ====================================

left,center,right = st.columns([1,3,1])

with center:

    components.html(
        svg,
        height=650,
        scrolling=False
    )# ====================================
# GAME PANEL
# ====================================

st.divider()

current_player = players[
    st.session_state.turn
]

st.subheader(
    f"🎯 Current Turn : {current_player.upper()}"
)

# ====================================
# DICE
# ====================================

dice_faces = {
    1:"⚀",
    2:"⚁",
    3:"⚂",
    4:"⚃",
    5:"⚄",
    6:"⚅"
}

col1,col2,col3 = st.columns([1,1,1])

with col2:

    st.markdown(
        f"""
        <h1 style='text-align:center'>
        {dice_faces[st.session_state.dice]}
        </h1>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🎲 Roll Dice",
        use_container_width=True
    ):

        st.session_state.dice = (
            random.randint(1,6)
        )

        st.rerun()

# ====================================
# CAPTURE LOGIC
# ====================================

def capture_tokens():

    token_map = {}

    for color in players:

        start = START_INDEX[color]

        for idx,pos in enumerate(
            st.session_state.tokens[color]
        ):

            if pos < 0:
                continue

            if pos >= len(PATH):
                continue

            board_pos = (
                start + pos
            ) % len(PATH)

            if board_pos in SAFE:
                continue

            if board_pos not in token_map:

                token_map[board_pos] = []

            token_map[board_pos].append(
                (color,idx)
            )

    for square,tokens in token_map.items():

        colors = set(
            x[0] for x in tokens
        )

        if len(colors) > 1:

            keeper = tokens[0]

            for victim in tokens[1:]:

                st.session_state.tokens[
                    victim[0]
                ][victim[1]] = -1

# ====================================
# WIN CHECK
# ====================================

def check_winner():

    for color in players:

        won = True

        for pos in st.session_state.tokens[color]:

            if pos < 57:
                won = False

        if won:

            st.balloons()

            st.success(
                f"🏆 {color.upper()} WINS!"
            )

            return True

    return False

# ====================================
# TOKEN BUTTONS
# ====================================

st.divider()

st.subheader(
    f"Move a {current_player.upper()} Token"
)

token_cols = st.columns(4)

for idx in range(4):

    with token_cols[idx]:

        token_pos = (
            st.session_state.tokens
            [current_player][idx]
        )

        if token_pos == -1:
            txt = "🏠 HOME"

        elif token_pos >= 57:
            txt = "🏆 FINISHED"

        else:
            txt = f"📍 {token_pos}"

        st.caption(txt)

        if st.button(
            f"Token {idx+1}",
            key=f"{current_player}_{idx}"
        ):

            move_token(
                current_player,
                idx
            )

            capture_tokens()

            if check_winner():
                st.stop()

            # extra turn on 6

            if st.session_state.dice != 6:

                st.session_state.turn = (
                    st.session_state.turn + 1
                ) % 4

            st.rerun()

# ====================================
# SCOREBOARD
# ====================================

st.divider()

st.subheader("📊 Token Status")

for color in players:

    st.write(
        f"**{color.upper()}** : "
        f"{st.session_state.tokens[color]}"
    )

# ====================================
# RESET GAME
# ====================================

st.divider()

if st.button(
    "🔄 Reset Game",
    use_container_width=True
):

    st.session_state.tokens = {
        "red":[-1,-1,-1,-1],
        "green":[-1,-1,-1,-1],
        "yellow":[-1,-1,-1,-1],
        "blue":[-1,-1,-1,-1]
    }

    st.session_state.turn = 0
    st.session_state.dice = 1

    st.rerun()
