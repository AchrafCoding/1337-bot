import requests
import re
import smtplib
from email.mime.text import MIMEText
from time import sleep

EMAIL = "karzitachraf8@gmail.com"
EMAIL_PASSWORD = "ACHRAF1337KA"
USERNAME_1337 = "hshxhdhbhxhd@gmail.com"
PASSWORD_1337 = "*9xgrwf#+GD2&T"

session = requests.Session()

HEADERS_GET = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-language": "fr,en-US;q=0.9,en;q=0.8",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

HEADERS_POST = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "accept-language": "fr,en-US;q=0.9,en;q=0.8",
    "referer": "https://candidature.1337.ma/users/sign_in",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

def send_alert():
    try:
        msg = MIMEText("GO NOW: https://candidature.1337.ma/meetings")
        msg["Subject"] = "1337 SLOT OPEN NOW!"
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(EMAIL, EMAIL_PASSWORD)
            s.send_message(msg)
        print("Email sent!")
    except Exception as e:
        print(f"Email error: {e}")

def getCSRF():
    try:
        response = session.get(
            "https://candidature.1337.ma/users/sign_in",
            headers=HEADERS_GET)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return ""
        result = re.search(r'name="csrf-token" content="(.+?)"', response.text)
        if result:
            return result.group(1)
        return ""
    except Exception as e:
        print(f"CSRF error: {e}")
        sleep(30)
        return ""

def login(csrf):
    try:
        response = session.post(
            "https://candidature.1337.ma/users/sign_in",
            data={
                "utf8": "✓",
                "authenticity_token": csrf,
                "user[email]": USERNAME_1337,
                "user[password]": PASSWORD_1337,
                "commit": "Se connecter"
            },
            headers=HEADERS_POST)
        if response.url != "https://candidature.1337.ma/meetings":
            print("Login failed!")
            return False
        print("Logged in!")
        return True
    except Exception as e:
        print(f"Login error: {e}")
        sleep(30)
        return False

def checkAvailability():
    try:
        response = session.get(
            "https://candidature.1337.ma/meetings",
            headers=HEADERS_GET)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return False
        if response.url != "https://candidature.1337.ma/meetings":
            print("Not logged in")
            return False
        if "places libres" in response.text:
            return False
        return True
    except Exception as e:
        print(f"Monitor error: {e}")
        sleep(30)
        return False

print("Starting 1337 monitor...")
csrf = getCSRF()
if csrf == "":
    print("Error getting CSRF token")
    exit(1)

if not login(csrf):
    print("Login failed - check credentials")
    exit(1)

while True:
    if checkAvailability():
        print("SLOT FOUND!")
        send_alert()
    else:
        print("No slot yet...")
    sleep(3)
