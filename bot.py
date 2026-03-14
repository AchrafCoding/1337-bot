import requests
import time
import smtplib
from email.mime.text import MIMEText

EMAIL = "karzitachraf8@gmail.com"
EMAIL_PASSWORD = "ACHRAF1337KA"
TWITTER_USER = "1337FIL"
NITTER_URL = f"https://nitter.net/{TWITTER_USER}/rss"

last_tweet = ""

def send_alert(tweet):
    try:
        msg = MIMEText(f"1337 just posted:\n\n{tweet}\n\nGO CHECK: https://admission.1337.ma")
        msg["Subject"] = "🚨 1337 TWEETED - CHECK NOW!"
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(EMAIL, EMAIL_PASSWORD)
            s.send_message(msg)
        print("Email sent!")
    except Exception as e:
        print(f"Email error: {e}")

print("Watching 1337 Twitter...")
while True:
    try:
        r = requests.get(NITTER_URL, timeout=10,
            headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            import re
            titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', r.text)
            if titles and len(titles) > 1:
                latest = titles[1]
                if latest != last_tweet:
                    print(f"New tweet: {latest}")
                    last_tweet = latest
                    send_alert(latest)
                else:
                    print("No new tweet...")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(60)
