import streamlit as st
from db_mysql import fetch_all_chats

st.set_page_config(page_title="Admin Panel Chatbot", page_icon="🧠", layout="wide")

st.title("🧠 Admin Panel Chatbot")
st.write("Lihat semua riwayat percakapan pengguna di sini.")

chats = fetch_all_chats()

if chats:
    for chat in chats:
        with st.expander(f"{chat['username']} | {chat['timestamp']}"):
            st.write(f"**User:** {chat['user_message']}")
            st.write(f"**Bot:** {chat['bot_response']}")
else:
    st.info("Belum ada data chat tersimpan.")
