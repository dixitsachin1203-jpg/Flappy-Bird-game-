import streamlit as st

st.set_page_config(page_title="Ludo Royale", layout="wide")

board_html = """
<div style="
width:700px;
height:700px;
margin:auto;
background:white;
border:8px solid black;
position:relative;
">

<!-- RED -->
<div style="
position:absolute;
top:0;
left:0;
width:280px;
height:280px;
background:#e53935;
display:flex;
justify-content:center;
align-items:center;
">
<div style="
width:180px;
height:180px;
background:white;
border-radius:15px;
"></div>
</div>

<!-- GREEN -->
<div style="
position:absolute;
top:0;
right:0;
width:280px;
height:280px;
background:#43a047;
display:flex;
justify-content:center;
align-items:center;
">
<div style="
width:180px;
height:180px;
background:white;
border-radius:15px;
"></div>
</div>

<!-- YELLOW -->
<div style="
position:absolute;
bottom:0;
left:0;
width:280px;
height:280px;
background:#fdd835;
display:flex;
justify-content:center;
align-items:center;
">
<div style="
width:180px;
height:180px;
background:white;
border-radius:15px;
"></div>
</div>

<!-- BLUE -->
<div style="
position:absolute;
bottom:0;
right:0;
width:280px;
height:280px;
background:#1e88e5;
display:flex;
justify-content:center;
align-items:center;
">
<div style="
width:180px;
height:180px;
background:white;
border-radius:15px;
"></div>
</div>

<!-- CENTER -->
<div style="
position:absolute;
left:280px;
top:280px;
width:140px;
height:140px;
background:conic-gradient(
red 0deg 90deg,
green 90deg 180deg,
blue 180deg 270deg,
yellow 270deg 360deg
);
clip-path:polygon(
50% 0%,
100% 50%,
50% 100%,
0% 50%
);
">
</div>

</div>
"""

st.markdown(
    "<h1 style='text-align:center;'>🎲 Ludo Royale</h1>",
    unsafe_allow_html=True
)

st.components.v1.html(board_html, height=750)
