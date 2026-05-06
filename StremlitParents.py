import streamlit as st
from datetime import date, timedelta

# --- CONFIG & THEMING ---
st.set_page_config(
    page_title="Elda | Family Life Ledger", 
    page_icon="🌿",
    layout="wide"
)

# Custom CSS for Elda Branding
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    .stApp { background-color: #FFFFFF; }
    
    /* Elda Logo Style */
    .logo-text {
        font-size: 32px;
        font-weight: 700;
        color: #1B5E20;
        letter-spacing: -1px;
    }
    .logo-dot { color: #81C784; }

    /* Clean Card Headers */
    .section-header {
        font-size: 16px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #1B5E20;
        background-color: #F8FAF8;
        padding: 10px 15px;
        border-radius: 8px;
        margin-top: 25px;
        border-bottom: 2px solid #E8F5E9;
    }

    /* Tab Customization */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #F9FAFB;
        border-radius: 8px;
        padding: 8px 16px;
        color: #4B5563;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1B5E20 !important;
        color: white !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAF8;
        border-right: 1px solid #E0E4E0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION (The "Generic" Engine) ---
with st.sidebar:
    st.markdown('<p class="logo-text">elda<span class="logo-dot">.</span></p>', unsafe_allow_html=True)
    st.subheader("⚙️ Dashboard Config")
    
    with st.expander("Family Details", expanded=True):
        parent_name = st.text_input("Parent's Name", "Mrs. Chawla")
        manager_name = st.text_input("Care Manager", "Vanshul Chawla")
        location = st.text_input("Location/Unit", "Gurgaon 4BHK")
        nri_location = st.text_input("Manager Location (Home)", "USA")

    with st.expander("Emergency Defaults"):
        primary_hosp = st.text_input("Preferred Hospital", "Fortis Memorial")
        city_doctor = st.text_input("Primary Physician", "Dr. Trehan")

# --- HEADER ---
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.markdown(f"### {parent_name}'s Life Ledger")
    st.caption(f"Managed by **{manager_name}** | {location}")

# --- TABS ---
tabs = st.tabs(["💊 Health", "🚗 Auto", "🏠 Home", "✨ Social", "🚨 Emergency", "🌐 Manager View"])

# --- TAB 1: HEALTH ---
with tabs[0]:
    st.markdown('<div class="section-header">Medical Inventory</div>', unsafe_allow_html=True)
    med_data = st.data_editor({
        "Medication": ["Telma 40", "Thyronorm 50"],
        "Schedule": ["Morning", "Empty Stomach"],
        "In Stock": [15, 30]
    }, use_container_width=True, num_rows="dynamic")

# --- TAB 2: AUTO ---
with tabs[1]:
    st.markdown('<div class="section-header">Vehicle & Transport</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Primary Vehicle", "Honda City")
        st.date_input("Insurance Expiry", date(2026, 12, 31))
    with c2:
        st.text_input("Preferred Driver/Service", "Personal Driver - Ramesh")

# --- TAB 3: HOME ---
with tabs[2]:
    st.markdown('<div class="section-header">Home Infrastructure</div>', unsafe_allow_html=True)
    systems = st.multiselect("Select Systems to Track", 
                            ["RO Purifier", "Inverter", "Main AC", "Geyser", "Chimney"],
                            default=["RO Purifier", "Main AC"])
    for s in systems:
        col_s1, col_s2 = st.columns(2)
        col_s1.date_input(f"Last Service: {s}", date.today())
        col_s2.text_input(f"Vendor for {s}", "Local Provider")

# --- TAB 4: SOCIAL ---
with tabs[3]:
    st.markdown('<div class="section-header">Routine & Wellness</div>', unsafe_allow_html=True)
    st.text_area("Weekly Routine Notes", f"Ensure {parent_name} is accompanied for park walks.")

# --- TAB 5: EMERGENCY ---
with tabs[4]:
    st.markdown('<div class="section-header">Crisis Protocol</div>', unsafe_allow_html=True)
    st.error(f"**Immediate Action:** Contact {primary_hosp}")
    st.info(f"**Doctor on Call:** {city_doctor}")

# --- TAB 6: NRI/MANAGER VIEW ---
with tabs[5]:
    st.markdown(f'<div class="section-header">{nri_location} Oversight Dashboard</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    m1.metric("Care Adherence", "98%")
    m2.metric("Inventory Alerts", "2 Low")

# --- GLOBAL SAVE ---
st.markdown("---")
if st.button("💾 SYNC TO ELDA CLOUD"):
    st.balloons()
    st.success(f"Dashboard for {parent_name} updated successfully.")