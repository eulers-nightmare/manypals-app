from database import get_connection
import bcrypt

UNI_DOMAIN = "@learner.manipal.edu"  # change this to your real university domain if needed

def is_uni_email(email):
    return email.endswith(UNI_DOMAIN)

def register_user(name, email, password):
    if not is_uni_email(email):
        return False, "Use your university email."

    conn = get_connection()
    c = conn.cursor()
    try:
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                  (name, email, hashed_pw.decode('utf-8')))
        conn.commit()
        return True, "Registered successfully."
    except Exception:
        return False, "Email already registered."
    finally:
        conn.close()

def login_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, email, password FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
        return (user[0], user[1], user[2])  # return ID, name, email
    return None
