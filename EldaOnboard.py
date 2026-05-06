import streamlit as st
from datetime import date, timedelta

# --- CONFIG ---
# Setting layout to 'centered' helps mobile devices focus content without side-scrolling
st.set_page_config(page_title="Elda | Life Ledger", page_icon="🌿", layout="centered")

if 'onboarded' not in st.session_state:
    st.session_state.onboarded = False

# --- RESPONSIVE STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    
    /* Logo scaling for mobile */
    .elda-logo { font-size: clamp(32px, 8vw, 42px); font-weight: 800; color: #1B5E20; letter-spacing: -2px; }
    .elda-dot { color: #81C784; font-size: clamp(36px, 10vw, 48px); }
    
    /* Optimized Headers */
    .section-header {
        font-size: 13px; font-weight: 700; text-transform: uppercase;
        color: #1B5E20; background-color: #F0F4F0;
        padding: 10px 15px; border-radius: 8px; margin-top: 15px; margin-bottom: 10px;
    }

    /* Force buttons to be easily tappable on mobile */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: 600;
    }

    /* Remove padding for small screens to maximize space */
    @media (max-width: 640px) {
        .reportview-container .main .block-container {
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO ---
st.markdown('<span class="elda-logo">elda</span><span class="elda-dot">.</span>', unsafe_allow_html=True)

if not st.session_state.onboarded:
    st.markdown("### 📝 Initial Setup")
    with st.form("onboarding"):
        p_name = st.text_input("Senior's Name", "Mrs. Chawla")
        p_age = st.text_input("Age", "62")
        p_loc = st.text_input("Society/Apartment", "Gurgaon")
        if st.form_submit_button("Launch Dashboard"):
            st.session_state.onboarded = True
            st.session_state.p_name = p_name
            st.session_state.p_age = p_age
            st.session_state.p_loc = p_loc
            st.rerun()
else:
    st.write(f"**{st.session_state.p_name}** ({st.session_state.p_age} yrs) | {st.session_state.p_loc}")
    
    # Tabs are natively responsive in Streamlit (they become a scrollable row on mobile)
    tabs = st.tabs(["💊 Health", "🏠 Home", "✨ Social", "🚨 Emergency", "🇺🇸 Manager"])

    # --- TAB 1: MEDICAL ---
    with tabs[0]:
        st.markdown('<div class="section-header">Medical Conditions & Meds</div>', unsafe_allow_html=True)
        conditions = st.multiselect("Select Conditions", 
                                   ["Diabetes", "Hypertension (High BP)", "Thyroid", "Arthritis", "Cholesterol", "Cardiac Care"])
        
        for condition in conditions:
            with st.expander(f"📋 Chart: {condition}", expanded=True):
                # Data editors are scrollable, which works well on mobile
                st.data_editor({
                    "Medicine": ["", ""],
                    "Dose": ["", ""],
                    "M": [False, False], "T": [False, False], "W": [False, False], 
                    "Th": [False, False], "F": [False, False], "S": [False, False], "Su": [False, False],
                    "Time": ["Morning", "Night"]
                }, key=f"med_{condition}", use_container_width=True, num_rows="dynamic")

    # --- TAB 2: HOME ---
    with tabs[1]:
        st.markdown('<div class="section-header">Appliance Registry</div>', unsafe_allow_html=True)
        appliance_list = [
            "RO Water Purifier", "Refrigerator", "Washing Machine", "Microwave", "AC (Master)",
            "AC (Guest)", "AC (Drawing)", "Geyser (Master)", "Geyser (Guest)", 
            "Chimney", "Inverter/UPS", "Television", "Air Purifier", "Dishwasher"
        ]
        selected_apps = st.multiselect("Appliances", appliance_list, default=["RO Water Purifier", "Inverter/UPS"])
        
        for app in selected_apps:
            # Using a container with border for a "card" feel on mobile
            with st.container(border=True):
                st.write(f"**{app}**")
                # On mobile, we avoid columns to prevent horizontal squashing
                st.text_input(f"Service Partner", placeholder="Name/Phone", key=f"vendor_{app}")
                st.date_input(f"Last Service", date.today(), key=f"date_{app}")
                st.selectbox("Current Status", ["Healthy", "Needs Service", "Broken"], key=f"status_{app}")

    # --- TAB 3: SOCIAL ---
    with tabs[2]:
        st.markdown('<div class="section-header">Social & Spiritual</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.subheader("Templates")
            st.checkbox("Temple (Weekly Thursday)")
            st.checkbox("Kitty Party (Monthly)")
            st.checkbox("Kirtan / Satsang")
            st.checkbox("Parlour / Grooming (Every 30 Days)")
        
        with st.container(border=True):
            st.subheader("Custom Activity")
            st.text_input("Type", placeholder="e.g. Physiotherapy")
            st.text_input("Frequency", placeholder="e.g. Every Monday")
            st.text_area("Specific Preferences", placeholder="e.g. Prefers driver Ramesh")

    # --- TAB 4: EMERGENCY ---
    with tabs[3]:
        st.markdown('<div class="section-header" style="background-color: #FFEBEE;">Crisis Directory</div>', unsafe_allow_html=True)
        
        # Medical & Family
        with st.container(border=True):
            st.subheader("🏥 Medical")
            st.text_input("Hospital", "Fortis Memorial, Gurgaon")
            st.text_input("ER Phone", "+91 124 XXX XXXX")
            st.text_input("Doctor", "Dr. Trehan")
            st.text_input("Dr. Phone", "")

        with st.container(border=True):
            st.subheader("👨‍👩‍👧‍👦 Family")
            st.text_input("Primary (Son)", "Vanshul Chawla | +1 XXX XXX XXXX")
            st.text_input("Nearby Relative", "Name | Phone")
        
        # Society & Local
        with st.container(border=True):
            st.subheader("🏢 Society & RWA")
            st.text_input("Security Desk", "Intercom: 001")
            st.text_input("RWA Emergency", "Name | Phone")
            st.text_input("Maintenance", "Phone")

        with st.container(border=True):
            st.subheader("👮 Local Services")
            st.text_input("Police Station", "Sector 53")
            st.text_input("Ambulance", "102 / Private")

    # --- TAB 5: MANAGER VIEW ---
    with tabs[4]:
        st.markdown('<div class="section-header">Manager Oversight</div>', unsafe_allow_html=True)
        # Metrics stack automatically
        st.metric("Medication Adherence", "100%")
        st.metric("Critical Tasks", "0 Pending")
        st.metric("Next Visit", "In 4 Days")
        
    st.markdown("---")
    if st.button("💾 SAVE & SYNC DASHBOARD"):
        st.balloons()
        st.success("Synced with Elda Ops Team.")
