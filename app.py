import streamlit as st
import random
import string

st.set_page_config(page_title="CBSE Results 2025", layout="centered")

# ------------------- STYLING -------------------
st.markdown("""
<style>
.header {
    background-color: #00a6a6;
    padding: 15px;
    color: white;
    font-size: 22px;
    font-weight: bold;
    text-align:center;
}
.title {
    text-align: center;
    font-size: 26px;
    font-weight: bold;
    margin-top: 10px;
}
.box {
    border: 1px solid #ccc;
    padding: 25px;
    border-radius: 10px;
    background-color: #f9f9f9;
}
.captcha {
    font-size: 20px;
    font-weight: bold;
    background-color: navy;
    color: white;
    padding: 5px 10px;
    display: inline-block;
}
.success-box {
    text-align:center;
    padding:40px;
    border-radius:15px;
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color:white;
}
.big-text {
    font-size:40px;
    font-weight:bold;
}
.rank {
    font-size:28px;
    margin-top:10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------- HEADER -------------------
st.markdown('<div class="header">Central Board of Secondary Education</div>', unsafe_allow_html=True)

# ------------------- CORRECT DATA (EDIT THIS) -------------------
CORRECT_DATA = {
    "roll": "1234567",
    "school": "76543",
    "admit": "ABC12345",
    "dob": "01/01/2010"
}

# ------------------- CAPTCHA -------------------
def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

if "captcha" not in st.session_state:
    st.session_state.captcha = generate_captcha()

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ------------------- RESULT PAGE -------------------
if st.session_state.submitted:
    st.markdown("""
    <div class="success-box">
        <div class="big-text">🎉 Congratulations 🎉</div>
        <p style="font-size:22px;">You scored <b>100%</b></p>
        <div class="rank">🏆 All India Rank #1 🏆</div>
        <p style="margin-top:20px;">Outstanding Performance!</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔙 Go Back"):
        st.session_state.submitted = False
        st.rerun()

else:
    # ------------------- FORM -------------------
    st.markdown('<div class="title">Secondary School Examination (Class X) Results 2025</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)

        roll = st.text_input("Your Roll Number")
        school = st.text_input("Your School Number")
        admit = st.text_input("Admit Card ID")
        dob = st.text_input("Date of Birth (DD/MM/YYYY)")
        pin_input = st.text_input("Enter Security Pin")

        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f'<div class="captcha">{st.session_state.captcha}</div>', unsafe_allow_html=True)
        with col2:
            if st.button("🔄 Refresh"):
                st.session_state.captcha = generate_captcha()

        col3, col4 = st.columns(2)
        with col3:
            submit = st.button("Submit")
        with col4:
            reset = st.button("Reset")

        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------- VALIDATION -------------------
    if submit:
        if (
            roll == CORRECT_DATA["roll"] and
            school == CORRECT_DATA["school"] and
            admit == CORRECT_DATA["admit"] and
            dob == CORRECT_DATA["dob"] and
            pin_input == st.session_state.captcha
        ):
            st.session_state.submitted = True
            st.rerun()
        else:
            st.error("❌ Invalid Credentials! Please check your details.")

    if reset:
        st.session_state.captcha = generate_captcha()
        st.rerun()

# ------------------- DISCLAIMER -------------------
st.markdown("""
---
**Disclaimer:** This is a demo project. Not an official CBSE result portal.
""")
