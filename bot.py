import requests
import time
import os
import smtplib
from email.mime.text import MIMEText

USERNAME = os.environ["USERNAME_1337"]
PASSWORD_1337 = os.environ["PASSWORD_1337"]
EMAIL = os.environ["EMAIL"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
MARKER = "Any available Check-ins will appear here"

def send_alert():
    try:
        msg = MIMEText("GO NOW: https://admission.1337.ma")
        msg["Subject"] = "1337 SLOT OPEN NOW!"
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(EMAIL, EMAIL_PASSWORD)
            s.send_message(msg)
        print("Email sent!")
    except Exception as e:
        print(f"Email error: {e}")

def check_slots(session):
    try:
        r = session.get("https://admission.1337.ma", timeout=10,
            headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            if MARKER not in r.text:
                print("SLOT FOUND!")
                send_alert()
                time.sleep(30)
            else:
                print("No slot yet...")
        else:
            print(f"Status: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def login():
    session = requests.Session()
    try:
        # Get login page first
        login_page = session.get("https://admission.1337.ma/users/sign_in",
            headers={"User-Agent": "Mozilla/5.0"})
        # Extract CSRF token
        import re
        token = re.search(
            r'name="authenticity_token" value="([^"]+)"',
            login_page.text)
        csrf = token.group(1) if token else ""
        # Login
        session.post("https://admission.1337.ma/users/sign_in", data={
            "user[login]": USERNAME,
            "user[password]": PASSWORD_1337,
            "authenticity_token": csrf
        }, headers={"User-Agent": "Mozilla/5.0"})
        print("Logged in!")
    except Exception as e:
        print(f"Login error: {e}")
    return session

print("Starting 1337 monitor...")
session = login()
count = 0
while True:
    check_slots(session)
    count += 1
    if count % 100 == 0:  # re-login every 100 checks
        session = login()
    time.sleep(3)
