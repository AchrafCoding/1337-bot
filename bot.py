import requests
import time
import smtplib
import re
from email.mime.text import MIMEText

EMAIL = "karzitachraf8@gmail.com"
EMAIL_PASSWORD = "lhpjnplcbvnsbcui"
USERNAME_1337 = "your1337email@gmail.com"
PASSWORD_1337 = "your1337password"

MARKER = "Any available Check-ins will appear here"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

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

def login():
    session = requests.Session()
    try:
        login_page = session.get(
            "https://admission.1337.ma/users/sign_in",
            headers=HEADERS, timeout=15)
        token = re.search(
            r'name="authenticity_token" value="([^"]+)"',
            login_page.text)
        csrf = token.group(1) if token else ""
        session.post(
            "https://admission.1337.ma/users/sign_in",
            data={
                "user[login]": USERNAME_1337,
                "user[password]": PASSWORD_1337,
                "authenticity_token": csrf
            },
            headers=HEADERS, timeout=15)
        print("Logged in!")
    except Exception as e:
        print(f"Login error: {e}")
    return session

print("Starting 1337 monitor...")
session = login()
count = 0
while True:
    try:
        r = session.get(
"https://admission.1337.ma/candidature/check-in",

            headers=HEADERS, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
    print(r.text[:300])  # print first 300 chars
    if MARKER not in r.text:
        print("SLOT FOUND!")

                send_alert()
                time.sleep(30)
            else:
                print("No slot yet...")
        elif r.status_code == 403:
            print("Re-logging in...")
            session = login()
    except Exception as e:
        print(f"Error: {e}")
    count += 1
    if count % 50 == 0:
        session = login()
    time.sleep(3)
