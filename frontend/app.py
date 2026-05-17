import streamlit as st
import requests
import pandas as pd

# 🔥 PAGE CONFIG
st.set_page_config(
    page_title="Student System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔥 REMOVE COLLAPSE BUTTON
st.markdown("""
<style>
[data-testid="collapsedControl"] {
    display: none;
}
section[data-testid="stSidebar"] {
    width: 250px !important;
}
section[data-testid="stSidebar"] > div {
    width: 250px !important;
}
</style>
""", unsafe_allow_html=True)

API_URL = "https://student-management-system-qxkq.onrender.com"
# API_URL = "http://127.0.0.1:8000"
st.write(f"{API_URL}/login")

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "signup"

if "token" not in st.session_state:
    st.session_state.token = None

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎓 Student System")
st.sidebar.markdown("### Navigation")

menu = None
if st.session_state.token:
    menu = st.sidebar.radio("", ["Dashboard", "Create", "Update", "Delete"])

    if st.sidebar.button("Logout"):
        st.session_state.page = "login"
        st.session_state.token = None
        st.rerun()

# ---------------- SIGNUP ----------------
if st.session_state.page == "signup":

    st.title("📝 Signup")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Signup 🚀"):
        if not username or not password:
            st.error("All fields required ❌")
        else:
            requests.post(
                f"{API_URL}/signup",
                params={"username": username, "password": password}
            )
            st.success("Signup successful ✅")
            st.session_state.page = "login"
            st.rerun()

    if st.button("Go to Login"):
        st.session_state.page = "login"
        st.rerun()

# ---------------- LOGIN ----------------
elif st.session_state.page == "login":

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login 🔑"):
        res = requests.post(
            f"{API_URL}/login",
            params={"username": username, "password": password}
        )
        
        st.write(res.status_code)
        st.write(res.text)
        try:
            data = res.json()
        except:
                st.error("Backend not responding properly")
                st.write(res.text)  # 🔥 shows real error
                st.stop()

        if "access_token" in data:
            st.session_state.token = data["access_token"]
            st.session_state.page = "app"
            st.rerun()
        else:
            st.error("Invalid credentials ❌")

# ---------------- MAIN APP ----------------
elif st.session_state.page == "app":

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    # 🔥 FETCH DATA
    res = requests.get(f"{API_URL}/students", headers=headers)
    try:
        data = res.json()
    except:
                st.error("Backend not responding properly")
                st.write(res.text)  # 🔥 shows real error
                st.stop()

    # ---------------- DASHBOARD ----------------
    if menu == "Dashboard":

        st.title("📊 Dashboard")

        if data:
            total = len(data)
            avg_age = sum([s["age"] for s in data]) / total

            col1, col2 = st.columns(2)
            col1.metric("Total Students", total)
            col2.metric("Average Age", round(avg_age, 2))

            # 🔍 SEARCH
            search = st.text_input("Search student")
            if search:
                data = [s for s in data if search.lower() in s["name"].lower()]

            # 📋 TABLE ONLY (clean UI)
            st.subheader("Student List")
            st.dataframe(pd.DataFrame(data))

        else:
            st.info("No students found")

    # ---------------- CREATE ----------------
    elif menu == "Create":

        st.title("➕ Add Student")

        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1)

        if st.button("Create 🚀"):
            requests.post(
                f"{API_URL}/students",
                params={"name": name, "age": age},
                headers=headers
            )
            st.success("Created ✅")
            st.rerun()

    # ---------------- UPDATE ----------------
    elif menu == "Update":

        st.title("✏️ Update Student")

        if data:
            student_options = {f"{s['id']} - {s['name']}": s['id'] for s in data}
            selected = st.selectbox("Select Student", list(student_options.keys()))
            student_id = student_options[selected]

            new_name = st.text_input("New Name")
            new_age = st.number_input("New Age", min_value=1)

            if st.button("Update"):
                requests.put(
                    f"{API_URL}/students/{student_id}",
                    params={"name": new_name, "age": new_age},
                    headers=headers
                )
                st.success("Updated ✅")
                st.rerun()

    # ---------------- DELETE ----------------
    elif menu == "Delete":

        st.title("❌ Delete Student")

        if data:
            student_options = {f"{s['id']} - {s['name']}": s['id'] for s in data}
            selected = st.selectbox("Select Student", list(student_options.keys()))
            student_id = student_options[selected]

            if st.button("Delete"):
                requests.delete(
                    f"{API_URL}/students/{student_id}",
                    headers=headers
                )
                st.warning("Deleted ⚠️")
                st.rerun()