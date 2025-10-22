import mysql.connector

# === Koneksi ke MySQL ===
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password="",         
        database="chatbot"   
    )

# === Buat tabel kalau belum ada ===
def create_table():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            user_message TEXT,
            bot_response TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

# === Simpan chat ===
def save_chat(username, user_input, bot_response):
    connection = get_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO chat_history (username, user_message, bot_response)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (username, user_input, bot_response))
    connection.commit()
    cursor.close()
    connection.close()

# === Ambil riwayat chat per user ===
def get_chat_history(username):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chat_history WHERE username = %s ORDER BY timestamp ASC", (username,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows
