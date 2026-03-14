import requests
import time
import smtplib
import re
from email.mime.text import MIMEText

EMAIL = "karzitachraf8@gmail.com"
EMAIL_PASSWORD = "lhpjnplcbvnsbcui"
USERNAME_1337 = "PUT_YOUR_1337_EMAIL"
PASSWORD_1337 = "PUT_YOUR_1337_PASSWORD"

MARKER = "De nouveaux creneaux ouvriront"
LOGIN_URL = "https://admission.1337.ma/users/sign_in"
CHECK_URL = "https://admission.1337.ma/candidature/check-in"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr-MA,fr;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}

def send_alert():
    try:
        msg = MIMEText("GO NOW: https://admission.1337.ma/candidature/check-in")
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
        login_page = session.get(LOGIN_URL, headers=HEADERS, timeout=15)
        token = re.search(r'name="authenticity_token" value="([^"]+)"', login_page.text)
        csrf = token.group(1) if token else ""
        resp = session.post(LOGIN_URL, data={
            "user_email": USERNAME_1337,
            "user_password": PASSWORD_1337,
            "authenticity_token": csrf,
            "commit": "Sign in"
        }, headers={**HEADERS,
            "Referer": LOGIN_URL,
            "Content-Type": "application/x-www-form-urlencoded"
        }, timeout=15, allow_redirects=True)
        if "sign_in" not in resp.url:
            print("Logged in!")
        else:
            print("Login failed!")
    except Exception as e:
        print(f"Login error: {e}")
    return session

print("Starting 1337 monitor...")
session = login()
count = 0

while True:
    try:
        r = session.get(CHECK_URL, headers=HEADERS, timeout=10)
        print(f"Status: {r.status_code} | URL: {r.url}")
        if r.status_code == 200:
            if "sign_in" in r.url:
                print("Session expired - re-logging...")
                session = login()
            elif MARKER not in r.text:
                print("SLOT FOUND!")
                send_alert()
                time.sleep(30)
            else:
                print("No slot yet...")
        elif r.status_code == 403:
            print("Blocked - waiting 30s...")
            time.sleep(30)
            session = login()
    except Exception as e:
        print(f"Error: {e}")
    count += 1
    if count % 100 == 0:
        session = login()
    time.sleep(3)
