import streamlit as st
from pymongo import MongoClient
import math

# --- CONFIG ---
st.set_page_config(page_title="Elda | Customer Directory", page_icon="📋", layout="centered")

MONGO_URI = st.secrets["MONGO_URI"]
PAGE_SIZE = 50

# --- RESPONSIVE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: 600;
    }
    .customer-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 8px;
        background: #fafafa;
    }
    .customer-card h4 { margin: 0 0 4px 0; font-size: 16px; }
    .customer-card p { margin: 0; font-size: 13px; color: #555; }
    @media (max-width: 640px) {
        .reportview-container .main .block-container {
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def get_mongo_collection():
    client = MongoClient(MONGO_URI)
    db = client["EldaOnboardPlatform"]
    return db["EldaCustomerOnboardData"]

# --- STATE ---
if "selected_customer" not in st.session_state:
    st.session_state.selected_customer = None
if "editing" not in st.session_state:
    st.session_state.editing = False
if "page" not in st.session_state:
    st.session_state.page = 0

# --- EDIT PAGE ---
if st.session_state.selected_customer and st.session_state.editing:
    customer = st.session_state.selected_customer

    if st.button("← Back to Details"):
        st.session_state.editing = False
        st.rerun()

    st.markdown(f"## ✏️ Edit: {customer.get('name', '')}")

    with st.form("edit_form"):
        st.subheader("👤 Profile")
        e_name = st.text_input("Name", customer.get("name", ""))
        e_age = st.text_input("Age", customer.get("age", ""))
        e_mobile = st.text_input("Mobile", customer.get("mobile", ""))
        e_location = st.text_input("Location", customer.get("location", ""))

        st.subheader("🚨 Emergency")
        em = customer.get("emergency", {})
        e_hospital = st.text_input("Hospital", em.get("hospital", ""))
        e_er_phone = st.text_input("ER Phone", em.get("er_phone", ""))
        e_doctor = st.text_input("Doctor", em.get("doctor", ""))
        e_dr_phone = st.text_input("Dr. Phone", em.get("dr_phone", ""))
        e_primary = st.text_input("Primary Contact", em.get("primary_contact", ""))
        e_relative = st.text_input("Nearby Relative", em.get("nearby_relative", ""))
        e_security = st.text_input("Security Desk", em.get("security_desk", ""))
        e_rwa = st.text_input("RWA Emergency", em.get("rwa_emergency", ""))
        e_maintenance = st.text_input("Maintenance", em.get("maintenance", ""))
        e_police = st.text_input("Police Station", em.get("police_station", ""))
        e_ambulance = st.text_input("Ambulance", em.get("ambulance", ""))

        st.subheader("✨ Social Activities")
        social = customer.get("social", {})
        activities = social.get("activities", [])
        num_activities = max(len(activities), 1)
        edited_activities = []
        for i in range(num_activities):
            act = activities[i] if i < len(activities) else {}
            st.markdown(f"**Activity {i+1}**")
            a_name = st.text_input("Activity Name", act.get("name", ""), key=f"ea_name_{i}")
            a_freq = st.text_input("Frequency", act.get("frequency", ""), key=f"ea_freq_{i}")
            a_desc = st.text_area("Description", act.get("description", ""), key=f"ea_desc_{i}")
            edited_activities.append({"name": a_name, "frequency": a_freq, "description": a_desc})

        st.subheader("🏠 Home Appliances")
        appliances = customer.get("home", {}).get("appliances", [])
        num_appliances = max(len(appliances), 1)
        edited_appliances = []
        for i in range(num_appliances):
            app = appliances[i] if i < len(appliances) else {}
            st.markdown(f"**Appliance {i+1}**")
            ap_name = st.text_input("Appliance Name", app.get("name", ""), key=f"eap_name_{i}")
            ap_vendor = st.text_input("Service Partner", app.get("vendor", ""), key=f"eap_vendor_{i}")
            ap_service = st.text_input("Last Service", app.get("last_service", ""), key=f"eap_service_{i}")
            ap_status = st.selectbox("Status", ["Healthy", "Needs Service", "Broken"],
                                     index=["Healthy", "Needs Service", "Broken"].index(app.get("status", "Healthy")) if app.get("status") in ["Healthy", "Needs Service", "Broken"] else 0,
                                     key=f"eap_status_{i}")
            edited_appliances.append({"name": ap_name, "vendor": ap_vendor, "last_service": ap_service, "status": ap_status})

        submitted = st.form_submit_button("💾 Save Changes")
        if submitted:
            collection = get_mongo_collection()
            updated_doc = {
                "name": e_name, "age": e_age, "mobile": e_mobile, "location": e_location,
                "emergency": {
                    "hospital": e_hospital, "er_phone": e_er_phone,
                    "doctor": e_doctor, "dr_phone": e_dr_phone,
                    "primary_contact": e_primary, "nearby_relative": e_relative,
                    "security_desk": e_security, "rwa_emergency": e_rwa,
                    "maintenance": e_maintenance, "police_station": e_police,
                    "ambulance": e_ambulance
                },
                "social": {"activities": [a for a in edited_activities if a["name"]]},
                "home": {"appliances": [a for a in edited_appliances if a["name"]]}
            }
            if customer.get("health"):
                updated_doc["health"] = customer["health"]
            collection.update_one(
                {"name": customer.get("name")},
                {"$set": updated_doc},
                upsert=True
            )
            st.session_state.selected_customer = updated_doc
            st.session_state.editing = False
            st.success("Customer updated!")
            st.rerun()

# --- DETAIL PAGE ---
elif st.session_state.selected_customer:
    customer = st.session_state.selected_customer

    if st.button("← Back to Directory"):
        st.session_state.selected_customer = None
        st.rerun()

    st.markdown(f"## {customer.get('name', 'Unknown')}")
    st.caption(f"📱 {customer.get('mobile', '')} | 📍 {customer.get('location', '')} | 🎂 Age: {customer.get('age', '')}")

    if st.button("✏️ Edit Customer"):
        st.session_state.editing = True
        st.rerun()

    st.markdown("---")

    # Stacked sections (mobile-friendly, no columns)
    with st.container(border=True):
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

    with st.container(border=True):
        st.subheader("✨ Social")
        social = customer.get("social", {})
        activities = social.get("activities", []) if social else []
        if activities:
            for act in activities:
                st.write(f"**{act.get('name', '')}** — {act.get('frequency', '')}")
                if act.get("description"):
                    st.caption(act["description"])
        else:
            st.info("No social data saved.")

    with st.container(border=True):
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

    with st.container(border=True):
        st.subheader("🏠 Home Appliances")
        appliances = customer.get("home", {}).get("appliances", [])
        if appliances:
            for app in appliances:
                st.write(f"**{app.get('name', '')}** — {app.get('status', '')} | Vendor: {app.get('vendor', 'N/A')} | Last: {app.get('last_service', 'N/A')}")
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

    if st.session_state.page >= total_pages:
        st.session_state.page = 0

    skip = st.session_state.page * PAGE_SIZE
    customers = list(collection.find(query, {"_id": 0}).skip(skip).limit(PAGE_SIZE))

    if not customers:
        st.warning("No customers found.")
        st.stop()

    # Mobile-friendly card layout instead of columns
    for i, c in enumerate(customers):
        with st.container(border=True):
            st.markdown(f"**{c.get('name', '')}**")
            st.caption(f"📱 {c.get('mobile', '')} | 📍 {c.get('location', '')} | Age: {c.get('age', '')}")
            if st.button("View →", key=f"view_{i}"):
                st.session_state.selected_customer = c
                st.rerun()

    # Pagination
    st.markdown("---")
    pcol1, pcol2, pcol3 = st.columns(3)
    with pcol1:
        if st.button("← Previous", disabled=(st.session_state.page == 0)):
            st.session_state.page -= 1
            st.rerun()
    with pcol2:
        st.markdown(f"<center><small>Page {st.session_state.page + 1}/{total_pages} ({total})</small></center>", unsafe_allow_html=True)
    with pcol3:
        if st.button("Next →", disabled=(st.session_state.page >= total_pages - 1)):
            st.session_state.page += 1
            st.rerun()
