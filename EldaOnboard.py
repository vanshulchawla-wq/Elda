import streamlit as st
from datetime import date, timedelta

# --- CONFIG ---
st.set_page_config(page_title="Elda | Life Ledger", page_icon="🌿", layout="wide")

if 'onboarded' not in st.session_state:
    st.session_state.onboarded = False

# --- STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    
    .elda-logo { font-size: 42px; font-weight: 800; color: #1B5E20; letter-spacing: -2px; }
    .elda-dot { color: #81C784; font-size: 48px; }
    .section-header {
        font-size: 14px; font-weight: 700; text-transform: uppercase;
        color: #1B5E20; background-color: #F0F4F0;
        padding: 8px 15px; border-radius: 5px; margin-top: 20px; margin-bottom: 10px;
    }
    .card {
        padding: 15px; border-radius: 10px; border: 1px solid #E0E0E0; background-color: #FAFAFA; margin-bottom: 10px;
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
        p_loc = st.text_input("Society/Apartment (e.g., DLF Crest, M3M Golfestate)", "Gurgaon")
        if st.form_submit_button("Launch Dashboard"):
            st.session_state.onboarded = True
            st.session_state.p_name = p_name
            st.session_state.p_age = p_age
            st.session_state.p_loc = p_loc
            st.rerun()
else:
    st.markdown(f"## {st.session_state.p_name}'s Life Ledger | {st.session_state.p_loc}")
    tabs = st.tabs(["💊 Medical & Health", "🏠 Home & Appliances", "✨ Social & Spiritual", "🚨 Emergency Contacts", "🇺🇸 Manager View"])

    # --- TAB 1: MEDICAL ---
    with tabs[0]:
        st.markdown('<div class="section-header">Chronic Conditions & Medications</div>', unsafe_allow_html=True)
        conditions = st.multiselect("Select Medical Conditions", 
                                   ["Diabetes", "Hypertension (High BP)", "Thyroid", "Arthritis", "Cholesterol", "Cardiac Care"])
        
        for condition in conditions:
            with st.expander(f"📋 Dosage Chart: {condition}", expanded=True):
                st.write(f"Weekly Schedule for {condition} management:")
                st.data_editor({
                    "Medicine Name": ["", ""],
                    "Dosage (mg)": ["", ""],
                    "Mon": [False, False], "Tue": [False, False], "Wed": [False, False], 
                    "Thu": [False, False], "Fri": [False, False], "Sat": [False, False], "Sun": [False, False],
                    "Time": ["Morning (Pre-Food)", "Night (Post-Food)"]
                }, key=f"med_{condition}", use_container_width=True, num_rows="dynamic")

    # --- TAB 2: HOME ---
    with tabs[1]:
        st.markdown('<div class="section-header">Appliance Maintenance Registry</div>', unsafe_allow_html=True)
        appliance_list = [
            "RO Water Purifier", "Refrigerator", "Washing Machine", "Microwave", "Air Conditioner (Master)",
            "Air Conditioner (Guest)", "Air Conditioner (Drawing Room)", "Geyser (Master Bath)", 
            "Geyser (Guest Bath)", "Kitchen Chimney", "Inverter/UPS", "Television", "Air Purifier", "Dishwasher"
        ]
        selected_apps = st.multiselect("Select Household Appliances", appliance_list, default=["RO Water Purifier", "Inverter/UPS"])
        
        for app in selected_apps:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1: st.text_input(f"{app}: Service Partner / Name", placeholder="e.g. Raju Plumber / Urban Company", key=f"vendor_{app}")
            with col2: st.date_input(f"Last Service Date", date.today(), key=f"date_{app}")
            with col3: st.selectbox("Status", ["Healthy", "Needs Service", "Broken"], key=f"status_{app}")

    # --- TAB 3: SOCIAL ---
    with tabs[2]:
        st.markdown('<div class="section-header">Recurring Social & Spiritual Events</div>', unsafe_allow_html=True)
        
        # Standard Templates
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.subheader("Templates")
            st.checkbox("Temple (Weekly Thursday)")
            st.checkbox("Kitty Party (Monthly)")
            st.checkbox("Kirtan / Satsang")
            st.checkbox("Parlour / Grooming (Every 30 Days)")
        
        with col_s2:
            st.subheader("Custom Preference")
            c_type = st.text_input("Activity Type", placeholder="e.g. Physiotherapy / Bridge Club")
            c_freq = st.text_input("Frequency", placeholder="e.g. Every Monday 4 PM")
            c_pref = st.text_area("Preferences", placeholder="e.g. Needs car with AC on high")

    # --- TAB 4: EMERGENCY ---
    with tabs[3]:
        st.markdown('<div class="section-header">Verified Crisis Directory</div>', unsafe_allow_html=True)
        
        # Category-based layout
        e_col1, e_col2 = st.columns(2)
        with e_col1:
            with st.container(border=True):
                st.subheader("🏥 Medical")
                st.text_input("Preferred Hospital", "Fortis Memorial, Gurgaon")
                st.text_input("Hospital ER Number", "+91 124 XXX XXXX")
                st.text_input("Primary Doctor", "Dr. Trehan")
                st.text_input("Doctor's Phone", "")

            with st.container(border=True):
                st.subheader("👨‍👩‍👧‍👦 Family & Relatives")
                st.text_input("Kids (Primary)", "Vanshul Chawla | +1 XXX XXX XXXX")
                st.text_input("Nearby Relative (Gurgaon/Delhi)", "Name | Phone")
        
        with e_col2:
            with st.container(border=True):
                st.subheader("🏢 Society & RWA")
                st.text_input("Society Security Desk", "Intercom: 001")
                st.text_input("RWA Emergency Head", "Name | Phone")
                st.text_input("Maintenance Office", "Phone")

            with st.container(border=True):
                st.subheader("👮 Local Services")
                st.text_input("Local Police Station", "Sector 53 Station")
                st.text_input("Preferred Ambulance", "102 / Private Provider")

    # --- TAB 5: MANAGER VIEW ---
    with tabs[4]:
        st.markdown('<div class="section-header">USA Monitoring Dashboard</div>', unsafe_allow_html=True)
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Medication Adherence", "100%")
        m_col2.metric("Critical Tasks", "0 Pending")
        m_col3.metric("Next Visit", "In 4 Days")
        
    st.markdown("---")
    if st.button("💾 SAVE & SYNC DASHBOARD"):
        st.balloons()
        st.success("Life Ledger data synced with Gurgaon Ops Team.")
