import smtplib
from email.mime.text import MIMEText
from random import randint

# --- Generate OTP ---
def generate_otp():
    return str(randint(100000, 999999))

# --- Send OTP via Gmail ---
def send_otp(to_email, otp):
    msg = MIMEText(f"Your ManyPals OTP is: {otp}")
    msg["Subject"] = "ManyPals Login Verification"
    msg["From"] = "epicmail75@gmail.com"
    msg["To"] = to_email

    # Gmail SMTP setup
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("epicmail75@gmail.com", "thfnimzcxnrafjoh")
    server.send_message(msg)
    server.quit()
