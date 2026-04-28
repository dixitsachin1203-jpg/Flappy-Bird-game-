import streamlit as st

# Set page configuration
st.set_page_config(page_title="CBSE Results 2025", layout="wide")

# Custom CSS for the teal header and styling
st.markdown("""
    <style>
    .main-header {
        background-color: #00b2b2;
        padding: 20px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 5px;
        margin-bottom: 30px;
    }
    .disclaimer {
        font-size: 12px;
        color: #555;
        text-align: justify;
        border-top: 1px solid #ddd;
        padding-top: 20px;
        margin-top: 20px;
    }
    </style>
    <div class="main-header">
        <div>
            <b>केन्द्रीय माध्यमिक शिक्षा बोर्ड</b><br>
            Central Board of Secondary Education
        </div>
        <div style="text-align: right;">
            <b>https://cbseresults.nic.in</b><br>
            Examination Results 2025
        </div>
    </div>
    """, unsafe_allow_index=True)

# Main container for the form
with st.container():
    st.markdown("<h4 style='text-align: center;'>Secondary School Examination (Class X) Results 2025</h4>", unsafe_allow_index=True)
    
    # Using columns to create the label-input alignment seen in the image
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("") # Spacer
        st.write("**Your Roll Number :**")
        st.write("**Your School Number :**")
        st.markdown("**Admit Card Id** <span style='color:blue; font-size:12px;'>(as given on your admit card)</span> **:**", unsafe_allow_index=True)
        st.markdown("**Date Of Birth** <span style='color:blue; font-size:12px;'>(DD/MM/YYYY)</span> **:**", unsafe_allow_index=True)
        st.markdown("**Enter Security Pin** <span style='color:blue; font-size:12px;'>(case sensitive)</span> **:**", unsafe_allow_index=True)
        st.write("**Security Pin :**")

    with col2:
        roll_no = st.text_input("Roll Number", label_visibility="collapsed")
        school_no = st.text_input("School Number", label_visibility="collapsed")
        admit_id = st.text_input("Admit Card Id", label_visibility="collapsed")
        dob = st.text_input("Date of Birth", label_visibility="collapsed")
        pin_input = st.text_input("Security Pin", label_visibility="collapsed")
        
        # Simulated Captcha Row
        cap_col1, cap_col2 = st.columns([1, 4])
        cap_col1.info("ZKJG20")
        if cap_col2.button("🔄"):
            st.rerun()

    # Buttons
    st.write("")
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([2, 1, 1, 2])
    with btn_col2:
        submit = st.button("Submit", type="primary", use_container_width=True)
    with btn_col3:
        reset = st.button("Reset", type="secondary", use_container_width=True)

    # Disclaimer text
    st.markdown("""
        <div class="disclaimer">
            <b>Disclaimer:</b> Neither NIC nor CBSE is responsible for any inadvertent error that may have crept in the results being published on Net. 
            The results published on net are for Immediate information to the examinees. These can not be treated as original mark sheets. 
            Original mark sheets have been issued by the Board separately.
        </div>
    """, unsafe_allow_index=True)

# Logic for Submit
if submit:
    if roll_no and school_no:
        st.success(f"Fetching results for Roll Number: {roll_no}...")
    else:
        st.error("Please fill in the required fields.")
