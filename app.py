import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(
    page_title="🎲 Ludo Royale",
    layout="wide"
)

# ----------------------------------
# Session State
# ----------------------------------

if "dice" not in st.session_state:
    st.session_state.dice = 1

if "turn" not in st.session_state:
    st.session_state.turn = 0

players = ["🔴 Red", "🟢 Green", "🟡 Yellow", "🔵 Blue"]

# ----------------------------------
# Header
# ----------------------------------

st.markdown(
    f"""
    <h1 style='text-align:center;color:#ff4b4b'>
    🎲 Ludo Royale
    </h1>
    """,
    unsafe_allow_html=True
)

# ----------------------------------
# Sidebar
# ----------------------------------

st.sidebar.title("Game Panel")

st.sidebar.success(
    f"Current Turn:\n\n{players[st.session_state.turn]}"
)

if st.sidebar.button("🎲 Roll Dice"):

    st.session_state.dice = random.randint(1, 6)

st.sidebar.metric(
    "Dice",
    st.session_state.dice
)

# ----------------------------------
# SVG Board
# ----------------------------------

cell = 40
size = 15 * cell

svg = f"""
<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">

<!-- Background -->
<rect width="{size}" height="{size}" fill="white"/>

<!-- Grid -->
"""

for r in range(15):
    for c in range(15):

        color = "#ffffff"

        # RED HOME
        if r < 6 and c < 6:
            color = "#ef5350"

        # GREEN HOME
        elif r < 6 and c > 8:
            color = "#4caf50"

        # YELLOW HOME
        elif r > 8 and c < 6:
            color = "#fdd835"

        # BLUE HOME
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
        """

# -------------------------------
# White home squares
# -------------------------------

homes = [
    (1.5,1.5),
    (9.5,1.5),
    (1.5,9.5),
    (9.5,9.5)
]

for x,y in homes:

    svg += f"""
    <rect
        x="{x*cell}"
        y="{y*cell}"
        width="{3*cell}"
        height="{3*cell}"
        rx="10"
        fill="white"
        stroke="black"
    />
    """

# -------------------------------
# Center Star
# -------------------------------

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
fill="red"/>

<polygon
points="360,300 300,300 300,360"
fill="green"/>

<polygon
points="300,360 300,300 240,300"
fill="blue"/>

<polygon
points="240,300 300,300 300,240"
fill="yellow"/>
"""

# -------------------------------
# Red lane
# -------------------------------

for r in range(1,7):
    svg += f"""
    <rect x="{6*cell}"
          y="{r*cell}"
          width="{cell}"
          height="{cell}"
          fill="#ef5350"
          stroke="black"/>
    """

# -------------------------------
# Green lane
# -------------------------------

for c in range(8,14):
    svg += f"""
    <rect x="{c*cell}"
          y="{6*cell}"
          width="{cell}"
          height="{cell}"
          fill="#4caf50"
          stroke="black"/>
    """

# -------------------------------
# Blue lane
# -------------------------------

for r in range(8,14):
    svg += f"""
    <rect x="{8*cell}"
          y="{r*cell}"
          width="{cell}"
          height="{cell}"
          fill="#42a5f5"
          stroke="black"/>
    """

# -------------------------------
# Yellow lane
# -------------------------------

for c in range(1,7):
    svg += f"""
    <rect x="{c*cell}"
          y="{8*cell}"
          width="{cell}"
          height="{cell}"
          fill="#fdd835"
          stroke="black"/>
    """

# ----------------------------------
# Example Tokens
# ----------------------------------

tokens = [
    (3,3,"red"),
    (4,4,"red"),

    (11,3,"green"),
    (10,4,"green"),

    (3,11,"yellow"),
    (4,10,"yellow"),

    (11,11,"blue"),
    (10,10,"blue"),
]

for x,y,color in tokens:

    svg += f"""
    <circle
        cx="{x*cell}"
        cy="{y*cell}"
        r="14"
        fill="{color}"
        stroke="black"
        stroke-width="2"
    />
    """

svg += "</svg>"

# ----------------------------------
# Center Board
# ----------------------------------

left, center, right = st.columns([1,3,1])

with center:
    components.html(
        svg,
        height=650,
        scrolling=False
    )

# ----------------------------------
# Controls
# ----------------------------------

st.divider()

cols = st.columns(4)

for i,p in enumerate(players):

    with cols[i]:
        st.markdown(
            f"""
            <div style="
            text-align:center;
            font-size:20px;
            font-weight:bold;">
            {p}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.button(
            "Move Token",
            key=f"move_{i}"
        )

# ----------------------------------
# Next Turn
# ----------------------------------

if st.button("Next Turn"):

    st.session_state.turn = (
        st.session_state.turn + 1
    ) % 4

    st.rerun()
