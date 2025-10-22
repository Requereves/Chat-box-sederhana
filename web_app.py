import streamlit as st
import pandas as pd
import json
# from chatbot import chatbot_response
from db_mysql import create_table
from admin_panel import show_admin_panel
from chatbot import chatbot_page


st.set_page_config(page_title="Chatbot App", page_icon="💬", layout="wide")

# === Load user admin ===
with open("users.json", "r", encoding="utf-8") as f:
    USERS = json.load(f)

# === Session State untuk login admin ===
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# === Sidebar Navigasi ===
st.sidebar.title("📂 Navigasi")
page = st.sidebar.radio("Pilih Halaman:", ["Chatbot", "Admin Panel"])

st.sidebar.markdown("---")

# === Halaman Chatbot  ===
if page == "Chatbot":
    st.subheader("💬 Halaman Chatbot")
    username = st.text_input("Masukkan username kamu:")

    if username:
        chatbot_page(username=username)
    else:
        st.info("Masukkan username dulu untuk mulai chat.")

# === Halaman Admin (perlu login) ===
elif page == "Admin Panel":
    if not st.session_state.admin_logged_in:
        st.subheader("🔐 Login Admin")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in USERS and USERS[username]["password"] == password and USERS[username]["role"] == "admin":
                st.session_state.admin_logged_in = True
                st.success("Login berhasil! 👑")
                st.rerun()
            else:
                st.error("Username atau password salah.")
    else:
        st.sidebar.success("✅ Admin login aktif")
        if st.sidebar.button("🚪 Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

        show_admin_panel()
