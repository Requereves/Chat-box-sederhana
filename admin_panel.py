import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db_mysql import get_all_chats, get_chat_summary, get_chat_count_per_user, get_chat_count_per_date


# === Fungsi utama untuk menampilkan halaman admin ===
def show_admin_panel():
    st.title("🧠 Admin Panel Chatbot")
    st.write("Lihat statistik dan semua riwayat percakapan pengguna di sini.")

    # === Ambil data dari database ===
    chats = get_all_chats()
    summary = get_chat_summary()

    if chats:
        df = pd.DataFrame(chats)

        # === Ringkasan Umum ===
        st.subheader("📋 Ringkasan")
        col1, col2 = st.columns(2)
        col1.metric("Total Chat", summary["total_chat"])
        col2.metric("Total Pengguna", summary["total_user"])

        st.markdown("---")

        # === Statistik Chat per User ===
        st.subheader("👥 Jumlah Chat per Pengguna")
        chat_user_df = get_chat_count_per_user()
        st.bar_chart(chat_user_df.set_index("username"))

        # === Statistik Chat per Tanggal ===
        st.subheader("📅 Aktivitas Chat per Tanggal")
        chat_date_df = get_chat_count_per_date()

        fig, ax = plt.subplots()
        ax.plot(chat_date_df["tanggal"], chat_date_df["total_chat"], marker="o", linestyle="-")
        ax.set_title("Tren Aktivitas Chat Harian")
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Jumlah Chat")
        st.pyplot(fig)

        st.markdown("---")

        # === Daftar Lengkap Chat ===
        st.subheader("🗂️ Riwayat Chat Lengkap")
        for chat in chats:
            with st.expander(f"👤 {chat['username']} | 🕒 {chat['timestamp']}"):
                st.write(f"**User:** {chat['user_message']}")
                st.write(f"**Bot:** {chat['bot_response']}")

        # Tombol ekspor CSV
        st.download_button(
            label="⬇️ Ekspor ke CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="riwayat_chat.csv",
            mime="text/csv"
        )

    else:
        st.info("Belum ada data chat tersimpan di database.")
