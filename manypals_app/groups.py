from database import get_connection
from group_chat import group_chat_ui
import streamlit as st

def group_ui(current_user):
    st.header("Groups")

    conn = get_connection()
    c = conn.cursor()

    # --- Create new group ---
    name = st.text_input("New group name")
    if st.button("Create Group"):
        if name.strip():
            c.execute("INSERT INTO groups (name, created_by) VALUES (?, ?)", (name.strip(), current_user[0]))
            conn.commit()
            st.success("Group created!")
        else:
            st.warning("Please enter a group name.")

    # --- Show existing groups ---
    st.subheader("All Groups")
    c.execute("SELECT id, name FROM groups")
    all_groups = c.fetchall()

    if not all_groups:
        st.info("No groups yet. Create one above.")
    else:
        for gid, gname in all_groups:
            st.write(f"📌 {gname}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Join {gname}", key=f"join_{gid}"):
                    c.execute("INSERT OR IGNORE INTO group_members (group_id, user_id) VALUES (?, ?)", (gid, current_user[0]))
                    conn.commit()
                    st.success(f"Joined {gname}!")
            with col2:
                if st.button(f"Open {gname}", key=f"open_{gid}"):
                    conn.close()
                    group_chat_ui(gid, current_user)
                    return
    # --- Show groups you belong to ---
    st.subheader("Your Groups")
    c.execute("""
        SELECT g.name
        FROM groups g
        JOIN group_members gm ON g.id = gm.group_id
        WHERE gm.user_id = ?
    """, (current_user[0],))
    joined = c.fetchall()

    if not joined:
        st.write("You haven't joined any groups yet.")
    else:
        for (gname,) in joined:
            st.write(f"• {gname}")

    conn.close()
