import streamlit as st
import datetime
import re
import random
import json
from db_mysql import save_chat, create_table

# === Load responses dari file JSON ===
with open("responses.json", "r", encoding="utf-8") as f:
    responses = json.load(f)

# === Halaman chatbot utama ===
def chatbot_page(username):
    # st.title("💬 Chatbot Sederhana")

    # Kalau username belum dikirim dari web utama → tampilkan input manual
    if not username:
        username = st.text_input("Masukkan username kamu:")

    if username:
        create_table()

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Tampilkan riwayat chat
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        # Input pesan baru
        if prompt := st.chat_input("Ketik pesan kamu..."):
            st.chat_message("user").write(prompt)
            response = chatbot_response(username, prompt)
            st.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.info("Masukkan username dulu untuk mulai chat.")


# === Fungsi logika chatbot ===
def chatbot_response(username, user_input):
    user_input = user_input.lower()

    if re.search(r'\b(halo|hai|hello|hallo)\b', user_input):
        response = random.choice(responses["greetings"])
    elif re.search(r'waktu|jam', user_input):
        now = datetime.datetime.now().strftime("%H:%M")
        response = random.choice(responses["jam_responses"]).format(now)
    elif re.search(r'tanggal|hari ini', user_input):
        today = datetime.date.today().strftime("%d %B %Y")
        response = random.choice(responses["tanggal_responses"]).format(today)
    elif re.search(r'(bye|dadah|selamat tinggal)', user_input):
        response = random.choice(responses["bye_responses"])
    elif re.search(r'(makanan|makan)\b', user_input):
        response = random.choice(responses["makanan"])
    elif re.search(r'(cuaca)\b', user_input):
        response = random.choice(responses["cuaca"])
    else:
        response = "Maaf, aku belum mengerti. Bisa ulangi lagi?"

    # Simpan ke database
    save_chat(username, user_input, response)
    return response
