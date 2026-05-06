import streamlit as st
from datetime import date, timedelta
from pymongo import MongoClient

# --- MONGO CONNECTION ---
MONGO_URI = st.secrets["MONGO_URI"]

@st.cache_resource
def get_mongo_collection():
    client = MongoClient(MONGO_URI)
    db = client["EldaOnboardPlatform"]
    return db["EldaCustomerOnboardData"]

def get_med_data(condition):
    """Transform data_editor state (with integer keys) into MongoDB-safe format."""
    raw = st.session_state.get(f"med_{condition}", {})
    if not isinstance(raw, dict):
        return {}
    rows = []
    edited = raw.get("edited_rows", {})
    # Base data template
    base_rows = [
        {"Medicine": "", "Dose": "", "M": False, "T": False, "W": False, "Th": False, "F": False, "S": False, "Su": False, "Time": "Morning"},
        {"Medicine": "", "Dose": "", "M": False, "T": False, "W": False, "Th": False, "F": False, "S": False, "Su": False, "Time": "Night"},
    ]
    for i, base in enumerate(base_rows):
        row = {**base, **edited.get(i, {})}
        rows.append(row)
    # Added rows
    for added in raw.get("added_rows", []):
        if added:
            rows.append(added)
    return rows

# --- CONFIG ---
st.set_page_config(page_title="Elda | Life Ledger", page_icon="🌿", layout="centered")

if 'onboarded' not in st.session_state:
    st.session_state.onboarded = False

# --- RESPONSIVE STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    .elda-logo { font-size: clamp(32px, 8vw, 42px); font-weight: 800; color: #1B5E20; letter-spacing: -2px; }
    .elda-dot { color: #81C784; font-size: clamp(36px, 10vw, 48px); }
    .section-header {
        font-size: 13px; font-weight: 700; text-transform: uppercase;
        color: #1B5E20; background-color: #F0F4F0;
        padding: 10px 15px; border-radius: 8px; margin-top: 15px; margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: 600;
    }
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
        p_mobile = st.text_input("Mobile", "9909987899")
        p_loc = st.text_input("Society/Apartment", "Gurgaon")
        if st.form_submit_button("Launch Dashboard"):
            st.session_state.onboarded = True
            st.session_state.p_name = p_name
            st.session_state.p_age = p_age
            st.session_state.p_mobile = p_mobile
            st.session_state.p_loc = p_loc
            # Save profile to MongoDB on onboard
            collection = get_mongo_collection()
            collection.update_one(
                {"name": p_name},
                {"$set": {"name": p_name, "age": p_age, "mobile": p_mobile, "location": p_loc}},
                upsert=True
            )
            st.rerun()
else:
    st.write(f"**{st.session_state.p_name}** ({st.session_state.p_age} yrs) | {st.session_state.p_loc}")
    
    tabs = st.tabs(["💊 Health", "🏠 Home", "✨ Social", "🚨 Emergency", "🇺🇸 Manager"])

    # --- TAB 1: MEDICAL ---
    with tabs[0]:
        st.markdown('<div class="section-header">Medical Conditions & Meds</div>', unsafe_allow_html=True)
        conditions = st.multiselect("Select Conditions", 
                                   ["Diabetes", "Hypertension (High BP)", "Thyroid", "Arthritis", "Cholesterol", "Cardiac Care"])
        
        for condition in conditions:
            with st.expander(f"📋 Chart: {condition}", expanded=True):
                st.data_editor({
                    "Medicine": ["", ""],
                    "Dose": ["", ""],
                    "M": [False, False], "T": [False, False], "W": [False, False], 
                    "Th": [False, False], "F": [False, False], "S": [False, False], "Su": [False, False],
                    "Time": ["Morning", "Night"]
                }, key=f"med_{condition}", width="stretch", num_rows="dynamic")

        if st.button("💾 Save Health Data", key="save_health"):
            collection = get_mongo_collection()
            med_data = {c: get_med_data(c) for c in conditions}
            collection.update_one(
                {"name": st.session_state.p_name},
                {"$set": {"health": {"conditions": conditions, "medications": med_data}}},
                upsert=True
            )
            st.success("Health data saved!")

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
            with st.container(border=True):
                st.write(f"**{app}**")
                st.text_input(f"Service Partner", placeholder="Name/Phone", key=f"vendor_{app}")
                st.date_input(f"Last Service", date.today(), key=f"date_{app}")
                st.selectbox("Current Status", ["Healthy", "Needs Service", "Broken"], key=f"status_{app}")

        if st.button("💾 Save Home Data", key="save_home"):
            collection = get_mongo_collection()
            appliances = [
                {
                    "name": app,
                    "vendor": st.session_state.get(f"vendor_{app}", ""),
                    "last_service": str(st.session_state.get(f"date_{app}", "")),
                    "status": st.session_state.get(f"status_{app}", "")
                } for app in selected_apps
            ]
            collection.update_one(
                {"name": st.session_state.p_name},
                {"$set": {"home": {"appliances": appliances}}},
                upsert=True
            )
            st.success("Home data saved!")

    # --- TAB 3: SOCIAL ---
    with tabs[2]:
        st.markdown('<div class="section-header">Social & Spiritual</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.subheader("Templates")
            st.checkbox("Temple (Weekly Thursday)", key="chk_temple")
            st.checkbox("Kitty Party (Monthly)", key="chk_kitty")
            st.checkbox("Kirtan / Satsang", key="chk_kirtan")
            st.checkbox("Parlour / Grooming (Every 30 Days)", key="chk_parlour")
        
        with st.container(border=True):
            st.subheader("Custom Activity")
            st.text_input("Type", placeholder="e.g. Physiotherapy", key="custom_type")
            st.text_input("Frequency", placeholder="e.g. Every Monday", key="custom_freq")
            st.text_area("Specific Preferences", placeholder="e.g. Prefers driver Ramesh", key="custom_prefs")

        if st.button("💾 Save Social Data", key="save_social"):
            collection = get_mongo_collection()
            collection.update_one(
                {"name": st.session_state.p_name},
                {"$set": {"social": {
                    "temple": st.session_state.get("chk_temple", False),
                    "kitty_party": st.session_state.get("chk_kitty", False),
                    "kirtan": st.session_state.get("chk_kirtan", False),
                    "parlour": st.session_state.get("chk_parlour", False),
                    "custom_type": st.session_state.get("custom_type", ""),
                    "custom_freq": st.session_state.get("custom_freq", ""),
                    "custom_prefs": st.session_state.get("custom_prefs", "")
                }}},
                upsert=True
            )
            st.success("Social data saved!")

    # --- TAB 4: EMERGENCY ---
    with tabs[3]:
        st.markdown('<div class="section-header" style="background-color: #FFEBEE;">Crisis Directory</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.subheader("🏥 Medical")
            st.text_input("Hospital", "Fortis Memorial, Gurgaon", key="em_hospital")
            st.text_input("ER Phone", "+91 124 XXX XXXX", key="em_er_phone")
            st.text_input("Doctor", "Dr. Trehan", key="em_doctor")
            st.text_input("Dr. Phone", "", key="em_dr_phone")

        with st.container(border=True):
            st.subheader("👨👩👧👦 Family")
            st.text_input("Primary (Son)", "Vanshul Chawla | +1 XXX XXX XXXX", key="em_primary")
            st.text_input("Nearby Relative", "Name | Phone", key="em_relative")
        
        with st.container(border=True):
            st.subheader("🏢 Society & RWA")
            st.text_input("Security Desk", "Intercom: 001", key="em_security")
            st.text_input("RWA Emergency", "Name | Phone", key="em_rwa")
            st.text_input("Maintenance", "Phone", key="em_maintenance")

        with st.container(border=True):
            st.subheader("👮 Local Services")
            st.text_input("Police Station", "Sector 53", key="em_police")
            st.text_input("Ambulance", "102 / Private", key="em_ambulance")

        if st.button("💾 Save Emergency Data", key="save_emergency"):
            collection = get_mongo_collection()
            collection.update_one(
                {"name": st.session_state.p_name},
                {"$set": {"emergency": {
                    "hospital": st.session_state.get("em_hospital", ""),
                    "er_phone": st.session_state.get("em_er_phone", ""),
                    "doctor": st.session_state.get("em_doctor", ""),
                    "dr_phone": st.session_state.get("em_dr_phone", ""),
                    "primary_contact": st.session_state.get("em_primary", ""),
                    "nearby_relative": st.session_state.get("em_relative", ""),
                    "security_desk": st.session_state.get("em_security", ""),
                    "rwa_emergency": st.session_state.get("em_rwa", ""),
                    "maintenance": st.session_state.get("em_maintenance", ""),
                    "police_station": st.session_state.get("em_police", ""),
                    "ambulance": st.session_state.get("em_ambulance", "")
                }}},
                upsert=True
            )
            st.success("Emergency data saved!")

    # --- TAB 5: MANAGER VIEW ---
    with tabs[4]:
        st.markdown('<div class="section-header">Manager Oversight</div>', unsafe_allow_html=True)
        st.metric("Medication Adherence", "100%")
        st.metric("Critical Tasks", "0 Pending")
        st.metric("Next Visit", "In 4 Days")
