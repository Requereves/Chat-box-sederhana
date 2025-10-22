import datetime
import re
import random
import json
from db_mysql import save_chat, create_table

# Load responses dari file JSON
with open("responses.json", "r", encoding="utf-8") as f:
    responses = json.load(f)

# === Fungsi Chatbot ===
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

    else:
        response = "Maaf, aku belum mengerti. Bisa ulangi lagi?"

    # Simpan ke database
    save_chat(username, user_input, response)
    return response

