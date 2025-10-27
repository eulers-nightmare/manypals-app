import streamlit as st
from database import init_db, get_connection
from auth import register_user, login_user
from chat import chat_ui
from groups import group_ui
from pathlib import Path

from pathlib import Path
MEDIA_PATH = Path(__file__).parent / "media_store"
MEDIA_PATH.mkdir(exist_ok=True)

import uuid
from otp_utils import generate_otp, send_otp

# Initialize
Path("uploads").mkdir(exist_ok=True)
init_db()

st.set_page_config(page_title="ManyPals", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

menu = ["Register", "Login"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Register")
    name = st.text_input("Full name")
    email = st.text_input("University email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        ok, msg = register_user(name, email, password)
        if ok:
            st.success(msg)
        else:
            st.error(msg)

elif choice == "Login":
    st.subheader("Login with OTP Verification")

    email = st.text_input("University Email")
    password = st.text_input("Password", type="password")

    if "otp_sent" not in st.session_state:
        st.session_state.otp_sent = False
    if "generated_otp" not in st.session_state:
        st.session_state.generated_otp = None

    if st.button("Send OTP"):
        user = login_user(email, password)
        if user:
            otp = generate_otp()
            st.session_state.generated_otp = otp
            send_otp(email, otp)
            st.session_state.otp_sent = True
            st.success(f"OTP sent to {email}")
        else:
            st.error("Invalid credentials")

    if st.session_state.otp_sent:
        entered_otp = st.text_input("Enter the 6-digit OTP")

        if st.button("Verify OTP"):
            if entered_otp == st.session_state.generated_otp:
                st.session_state.user = login_user(email, password)
                st.success("OTP verified. Logged in successfully.")
                st.session_state.otp_sent = False
            else:
                st.error("Incorrect OTP. Try again.")


if st.session_state.user:
    st.sidebar.success(f"Logged in as {st.session_state.user[1]}")
    feature = st.sidebar.radio("Go to", ["Chat", "Groups", "Photo"])

    if feature == "Chat":
        chat_ui(st.session_state.user)

    elif feature == "Groups":
        group_ui(st.session_state.user)

    elif feature == "Photo":
        st.header("Share Photo")

        uploaded = st.file_uploader("Upload image", type=["png","jpg","jpeg"])
        caption = st.text_input("Caption")

        if uploaded and st.button("Post"):
            unique_name = f"{uuid.uuid4().hex}_{uploaded.name}"
            path = MEDIA_PATH / unique_name
            with open(path, "wb") as f:
                f.write(uploaded.getbuffer())

            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO posts (user_id, image_path, caption) VALUES (?, ?, ?)",
                      (st.session_state.user[0], path, caption))
            conn.commit()
            conn.close()
            st.success("Posted!")

        st.subheader("Recent posts")
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT image_path, caption FROM posts ORDER BY created_at DESC LIMIT 10")
        if st.session_state.user:
            for img, cap in c.fetchall():
                st.image(img, width=300)
                st.caption(cap)
        else:
            st.warning("Please log in to view media.")

        conn.close()
