import streamlit as st
from datetime import date, timedelta

# --- CONFIG & THEMING ---
st.set_page_config(
    page_title="Elda | Onboarding", 
    page_icon="🌿",
    layout="wide"
)

# Initialize Session State for Onboarding
if 'onboarded' not in st.session_state:
    st.session_state.onboarded = False

# Custom CSS for Elda Branding & Better Logo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif;
    }

    /* ELDA LOGO DESIGN */
    .logo-container {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    .elda-logo {
        font-family: 'Outfit', sans-serif;
        font-size: 42px;
        font-weight: 800;
        color: #1B5E20;
        letter-spacing: -2px;
    }
    .elda-dot {
        color: #81C784;
        font-size: 48px;
    }
    .tagline {
        font-size: 14px;
        color: #666;
        margin-top: -10px;
        margin-left: 2px;
        font-style: italic;
    }

    /* Section Headers */
    .section-header {
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        color: #1B5E20;
        background-color: #F0F4F0;
        padding: 8px 15px;
        border-radius: 5px;
        margin-top: 20px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #1B5E20;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- THE ELDA LOGO ---
st.markdown("""
    <div class="logo-container">
        <div>
            <span class="elda-logo">elda</span><span class="elda-dot">.</span>
            <p class="tagline">Concierge for Modern Aging</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- ONBOARDING LOGIC ---
if not st.session_state.onboarded:
    st.markdown("### 📝 Member Onboarding")
    st.info("Welcome to Elda. Please confirm the household details to begin life orchestration.")
    
    with st.form("onboarding_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Senior Details**")
            p_name = st.text_input("Senior's Full Name", "Mrs. Chawla")
            p_age = st.number_input("Age", min_value=50, max_value=100, value=62)
            p_lang = st.multiselect("Preferred Languages", ["Hindi", "English", "Punjabi"], default=["Hindi", "English"])
        
        with col2:
            st.markdown("**Household Context**")
            p_loc = st.text_input("Gurgaon Address / Society", "DLF Phase 5")
            p_house = st.selectbox("Property Type", ["4BHK Apartment", "3BHK Apartment", "Independent Villa", "Other"])
            p_manager = st.text_input("Emergency Contact (Child)", "Vanshul Chawla")

        submitted = st.form_submit_button("Start Life Ledger")
        if submitted:
            st.session_state.onboarded = True
            st.session_state.p_name = p_name
            st.session_state.p_loc = p_loc
            st.rerun()

# --- MAIN DASHBOARD (Unlocked after Onboarding) ---
else:
    # Sidebar for quick info
    with st.sidebar:
        st.success(f"📍 {st.session_state.p_name}")
        st.write(f"**Location:** {st.session_state.p_loc}")
        if st.button("Reset Onboarding"):
            st.session_state.onboarded = False
            st.rerun()

    st.markdown(f"## {st.session_state.p_name}'s Management Dashboard")
    
    # 5 Main Tabs
    tabs = st.tabs(["💊 Health", "🏠 Home", "✨ Social", "🚨 Emergency", "🇺🇸 NRI Oversight"])

    with tabs[0]:
        st.markdown('<div class="section-header">Medicine & Health</div>', unsafe_allow_html=True)
        st.data_editor({
            "Medicine": ["Telma 40", "Thyronorm 50"],
            "Schedule": ["Morning", "Empty Stomach"],
            "Stock": [15, 30]
        }, use_container_width=True)

    with tabs[1]:
        st.markdown('<div class="section-header">Infrastructure (4BHK Management)</div>', unsafe_allow_html=True)
        st.multiselect("Select Assets", ["RO Purifier", "Inverter", "AC - Master", "Geyser"], default=["RO Purifier"])
        st.date_input("Next Service Date")

    with tabs[2]:
        st.markdown('<div class="section-header">Religious & Social Preferences</div>', unsafe_allow_html=True)
        st.text_input("Preferred Temple", "Sai Ka Angan")
        st.checkbox("Needs Driver for Thursdays")

    with tabs[3]:
        st.markdown('<div class="section-header">Emergency Protocols</div>', unsafe_allow_html=True)
        st.error("Hospital: Fortis Memorial, Gurgaon")
        st.warning("Primary Physician: Dr. Trehan")

    with tabs[4]:
        st.markdown('<div class="section-header">USA Manager View</div>', unsafe_allow_html=True)
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Safety Score", "100%")
        col_m2.metric("Task Completion", "92%")

    st.markdown("---")
    if st.button("💾 SYNC TO ELDA CLOUD"):
        st.balloons()
