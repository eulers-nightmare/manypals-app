from database import get_connection
import streamlit as st
from crypto_utils import encrypt_message, decrypt_message

def chat_ui(current_user):
    st.header("Chat")

    conn = get_connection()
    c = conn.cursor()

    # List other users
    c.execute("SELECT id, name FROM users WHERE id != ?", (current_user[0],))
    users = c.fetchall()

    if not users:
        st.write("No other users yet.")
        return

    friend = st.selectbox("Select friend", users, format_func=lambda x: x[1])
    message = st.text_input("Message")

    if st.button("Send"):
        if message.strip():
            enc_msg = encrypt_message(message)
            c.execute("INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)",
                      (current_user[0], friend[0], enc_msg))
            conn.commit()
            st.success("Message sent!")

    st.subheader("Conversation")
    c.execute("""
        SELECT sender_id, content, timestamp FROM messages
        WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)
        ORDER BY timestamp
    """, (current_user[0], friend[0], friend[0], current_user[0]))

    for sender, enc_msg, ts in c.fetchall():
        try:
            msg = decrypt_message(enc_msg)
        except Exception:
            msg = "[Encrypted]"
        who = "You" if sender == current_user[0] else friend[1]
        st.write(f"**{who}:** {msg}  _({ts})_")

    conn.close()
