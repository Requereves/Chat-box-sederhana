import streamlit as st
import pandas as pd
from chatbot import chatbot_response
from db_mysql import save_chat, create_table, get_chat_history, get_connection


# def load_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# load_css("style/custom.css")

# === Konfigurasi Halaman ===
st.set_page_config(page_title="Chatbot Sederhana 🤖", page_icon="💬", layout="centered")

# === Sidebar Navigasi ===
st.sidebar.title("🧭 Navigasi")
page = st.sidebar.radio("Pilih Halaman:", ["💬 Chatbot", "🧠 Admin Panel"])

create_table()  # pastikan tabel ada

# === Halaman Chatbot ===
if page == "💬 Chatbot":
    st.title("💬 Chatbot Sederhana ")

    username = st.text_input("Masukkan username kamu:")

    if username:
        st.write(f"Halo **{username}**, silakan mulai chat!")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Ketik pesan kamu..."):
            st.chat_message("user").write(prompt)
            response = chatbot_response(username, prompt)
            st.chat_message("assistant").write(response)

            save_chat(username, prompt, response)
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.info("Masukkan username dulu untuk mulai chat.")

# === Halaman Admin Panel ===
elif page == "🧠 Admin Panel":
    st.title("🧠 Admin Panel - Riwayat Chat")

    # === Login sederhana ===
    password = st.text_input("Masukkan password admin:", type="password")
    if password != "admin123":  # ganti dengan password rahasia kamu
        st.warning("Masukkan password untuk mengakses panel admin.")
        st.stop()

    # === Jika password benar, tampilkan panel ===
    st.success("Login berhasil ✅")

    with st.expander("🔍 Filter Chat"):
        username_filter = st.text_input("Cari berdasarkan username (kosongkan untuk semua):")

    connection = get_connection()
    query = "SELECT * FROM chat_history"
    params = ()

    if username_filter:
        query += " WHERE username = %s"
        params = (username_filter,)

    query += " ORDER BY timestamp DESC"

    df = pd.read_sql(query, connection, params=params)
    connection.close()

    if df.empty:
        st.warning("Belum ada chat tersimpan di database.")
    else:
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "📥 Unduh Chat sebagai CSV",
            data=df.to_csv(index=False),
            file_name="chat_history.csv",
            mime="text/csv",
        )
