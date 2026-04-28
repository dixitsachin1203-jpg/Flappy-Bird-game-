import streamlit as st
import random
import string

# Page config
st.set_page_config(page_title="CBSE Results 2025", layout="centered")

# Custom CSS for styling (to mimic the page)
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        margin-top: 10px;
    }
    .header {
        background-color: #00a6a6;
        padding: 15px;
        color: white;
        font-size: 20px;
        font-weight: bold;
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
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header">Central Board of Secondary Education</div>', unsafe_allow_html=True)

# Title
st.markdown('<div class="title">Secondary School Examination (Class X) Results 2025</div>', unsafe_allow_html=True)

# Generate CAPTCHA
def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

if "captcha" not in st.session_state:
    st.session_state.captcha = generate_captcha()

# Form container
with st.container():
    st.markdown('<div class="box">', unsafe_allow_html=True)

    roll = st.text_input("Your Roll Number")
    school = st.text_input("Your School Number")
    admit = st.text_input("Admit Card ID (as given on your admit card)")
    dob = st.text_input("Date of Birth (DD/MM/YYYY)")
    pin_input = st.text_input("Enter Security Pin (case sensitive)")

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

# Logic
if submit:
    if pin_input == st.session_state.captcha:
        st.success("Form submitted successfully! (Demo only)")
        st.write("Roll:", roll)
        st.write("School:", school)
        st.write("Admit ID:", admit)
        st.write("DOB:", dob)
    else:
        st.error("Invalid Security Pin!")

if reset:
    st.session_state.captcha = generate_captcha()
    st.experimental_rerun()

# Disclaimer
st.markdown("""
---
**Disclaimer:** Neither NIC nor CBSE is responsible for any inadvertent error that may have crept in the results being published on Net. These cannot be treated as original mark sheets.
""")
