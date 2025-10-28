import streamlit as st
from database import get_connection
from crypto_utils import encrypt_message, decrypt_message

def group_chat_ui(group_id, current_user):
    st.subheader("Group Chat")

    conn = get_connection()
    c = conn.cursor()

    # --- Message input ---
    message = st.text_input("Type your message:")
    if st.button("Send", key=f"send_{group_id}"):
        if message.strip():
            encrypted = encrypt_message(message.strip())
            c.execute(
                "INSERT INTO group_messages (group_id, user_id, message) VALUES (?, ?, ?)",
                (group_id, current_user[0], encrypted)
            )
            conn.commit()
            st.write("✅ Inserted message into DB:", encrypted)
            st.success("Message sent!")
        else:
            st.warning("Message cannot be empty.")

    st.divider()
    st.subheader("Messages")

    # --- Fetch messages ---
    c.execute("""
        SELECT u.name, gm.message, gm.created_at
        FROM group_messages gm
        JOIN users u ON gm.user_id = u.id
        WHERE gm.group_id = ?
        ORDER BY gm.created_at ASC
    """, (group_id,))
    messages = c.fetchall()

    if not messages:
        st.info("No messages yet. Start the conversation!")
    else:
        for sender, msg, ts in messages:
            try:
                decrypted = decrypt_message(msg)
            except Exception:
                decrypted = msg  # fallback if message wasn't encrypted
            st.markdown(f"**{sender}**: {decrypted}  \n*({ts})*")

    conn.close()
