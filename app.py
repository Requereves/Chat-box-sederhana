# import streamlit as st
# from chatbot import chatbot_response, save_chat

# st.title("🤖 Chatbot Sederhana")

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# user_input = st.text_input("Kamu:", "")

# if st.button("Kirim") and user_input.strip() != "":
#     response = chatbot_response(user_input)
#     st.session_state.chat_history.append(("Kamu", user_input))
#     st.session_state.chat_history.append(("Bot", response))
#     save_chat(user_input, response)

# for sender, message in st.session_state.chat_history:
#     if sender == "Kamu":
#         st.markdown(f"🧑 **{sender}:** {message}")
#     else:
#         st.markdown(f"🤖 **{sender}:** {message}")
