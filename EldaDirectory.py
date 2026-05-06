import streamlit as st
from pymongo import MongoClient
import math

# --- CONFIG ---
st.set_page_config(page_title="Elda | Customer Directory", page_icon="📋", layout="wide")

MONGO_URI = "mongodb+srv://elda:eldaonboard.streamlit.app@elda.wzcx5kq.mongodb.net/?appName=Elda"
PAGE_SIZE = 50

@st.cache_resource
def get_mongo_collection():
    client = MongoClient(MONGO_URI)
    db = client["EldaOnboardPlatform"]
    return db["EldaCustomerOnboardData"]

# --- STATE ---
if "selected_customer" not in st.session_state:
    st.session_state.selected_customer = None
if "page" not in st.session_state:
    st.session_state.page = 0

# --- DETAIL PAGE ---
if st.session_state.selected_customer:
    customer = st.session_state.selected_customer

    if st.button("← Back to Directory"):
        st.session_state.selected_customer = None
        st.rerun()

    st.markdown(f"## {customer.get('name', 'Unknown')}")
    st.caption(f"{customer.get('mobile', '')} | {customer.get('location', '')} | Age: {customer.get('age', '')}")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🚨 Emergency")
        em = customer.get("emergency", {})
        if em:
            for label, key in [("Hospital", "hospital"), ("ER Phone", "er_phone"), ("Doctor", "doctor"),
                               ("Dr. Phone", "dr_phone"), ("Primary Contact", "primary_contact"),
                               ("Nearby Relative", "nearby_relative"), ("Security Desk", "security_desk"),
                               ("RWA Emergency", "rwa_emergency"), ("Maintenance", "maintenance"),
                               ("Police Station", "police_station"), ("Ambulance", "ambulance")]:
                val = em.get(key, "")
                if val:
                    st.write(f"**{label}:** {val}")
        else:
            st.info("No emergency data saved.")

    with col2:
        st.subheader("✨ Social")
        social = customer.get("social", {})
        if social:
            activities = []
            if social.get("temple"): activities.append("Temple")
            if social.get("kitty_party"): activities.append("Kitty Party")
            if social.get("kirtan"): activities.append("Kirtan/Satsang")
            if social.get("parlour"): activities.append("Parlour/Grooming")
            st.write(f"**Activities:** {', '.join(activities) if activities else 'None selected'}")
            if social.get("custom_type"):
                st.write(f"**Custom:** {social['custom_type']} ({social.get('custom_freq', '')})")
            if social.get("custom_prefs"):
                st.write(f"**Preferences:** {social['custom_prefs']}")
        else:
            st.info("No social data saved.")

    st.subheader("💊 Health")
    health = customer.get("health", {})
    if health:
        st.write(f"**Conditions:** {', '.join(health.get('conditions', []))}")
        meds = health.get("medications", {})
        for condition, rows in meds.items():
            with st.expander(f"📋 {condition}"):
                if isinstance(rows, list) and rows:
                    st.dataframe(rows, use_container_width=True, hide_index=True)
                else:
                    st.write("No medication data.")
    else:
        st.info("No health data saved.")

    st.subheader("🏠 Home Appliances")
    appliances = customer.get("home", {}).get("appliances", [])
    if appliances:
        st.dataframe(appliances, use_container_width=True, hide_index=True)
    else:
        st.info("No home data saved.")

# --- LISTING PAGE ---
else:
    st.markdown("## 📋 Elda Customer Directory")

    search_phone = st.text_input("🔍 Search by Phone Number", placeholder="Enter mobile number...")

    collection = get_mongo_collection()
    if search_phone:
        query = {"mobile": {"$regex": search_phone}}
    else:
        query = {}

    total = collection.count_documents(query)
    total_pages = max(1, math.ceil(total / PAGE_SIZE))

    # Reset page if out of bounds
    if st.session_state.page >= total_pages:
        st.session_state.page = 0

    # Fetch current page
    skip = st.session_state.page * PAGE_SIZE
    customers = list(collection.find(query, {"_id": 0}).skip(skip).limit(PAGE_SIZE))

    if not customers:
        st.warning("No customers found.")
        st.stop()

    # Header row
    header = st.columns([3, 1, 2, 3, 1])
    header[0].markdown("**Name**")
    header[1].markdown("**Age**")
    header[2].markdown("**Mobile**")
    header[3].markdown("**Location**")
    header[4].markdown("**Action**")

    # Customer rows
    for i, c in enumerate(customers):
        col1, col2, col3, col4, col5 = st.columns([3, 1, 2, 3, 1])
        col1.write(c.get("name", ""))
        col2.write(c.get("age", ""))
        col3.write(c.get("mobile", ""))
        col4.write(c.get("location", ""))
        if col5.button("View", key=f"view_{i}"):
            st.session_state.selected_customer = c
            st.rerun()

    # Pagination controls
    st.markdown("---")
    pcol1, pcol2, pcol3 = st.columns([1, 2, 1])
    with pcol1:
        if st.button("← Previous", disabled=(st.session_state.page == 0)):
            st.session_state.page -= 1
            st.rerun()
    with pcol2:
        st.markdown(f"<center>Page {st.session_state.page + 1} of {total_pages} ({total} customers)</center>", unsafe_allow_html=True)
    with pcol3:
        if st.button("Next →", disabled=(st.session_state.page >= total_pages - 1)):
            st.session_state.page += 1
            st.rerun()
