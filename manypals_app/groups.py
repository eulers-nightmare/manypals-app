from database import get_connection
import streamlit as st

def group_ui(current_user):
    st.header("Groups")

    conn = get_connection()
    c = conn.cursor()

    # Create new group
    name = st.text_input("New group name")

    if st.button("Create Group"):
        if name.strip():
            c.execute("INSERT INTO groups (name, created_by) VALUES (?, ?)", (name.strip(), current_user[0]))
            conn.commit()
            st.success("Group created!")
        else:
            st.warning("Please enter a group name.")

    st.subheader("Groups you belong to")
    c.execute("""
        SELECT g.id, g.name
        FROM groups g
        JOIN group_members gm ON g.id = gm.group_id
        WHERE gm.user_id = ?
    """, (current_user[0],))
    rows = c.fetchall()

    if not rows:
        st.write("You haven't joined any groups yet.")
    else:
        for r in rows:
            st.write(f"• {r[1]}")

    conn.close()
