import requests
import time
import os
import smtplib
from email.mime.text import MIMEText

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["EMAIL_PASSWORD"]
MARKER = "Any available Check-ins will appear here"
URL = "https://admission.1337.ma"

def alert():
    msg = MIMEText("GO NOW: https://admission.1337.ma")
    msg["Subject"] = "1337 SLOT OPEN NOW!"
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(EMAIL, PASSWORD)
        s.send_message(msg)
    print("Email sent!")

print("Watching 1337...")
while True:
    try:
        r = requests.get(URL, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if MARKER not in r.text:
            print("SLOT FOUND!")
            alert()
            time.sleep(30)
        else:
            print("No slot yet...")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(3)
