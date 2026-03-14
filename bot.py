import requests
import time
import smtplib
import re
from email.mime.text import MIMEText

EMAIL = "karzitachraf8@gmail.com"
EMAIL_PASSWORD = "lhpjnplcbvnsbcui"

NITTER_INSTANCES = [
    "https://nitter.net/1337FIL/rss",
    "https://nitter.privacydev.net/1337FIL/rss",
    "https://nitter.poast.org/1337FIL/rss",
]

last_tweet = ""

def send_alert(tweet):
    try:
        msg = MIMEText(f"1337 just posted:\n\n{tweet}\n\nGO NOW: https://admission.1337.ma/candidature/check-in")
        msg["Subject"] = "🚨 1337 TWEETED - GO NOW!"
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(EMAIL, EMAIL_PASSWORD)
            s.send_message(msg)
        print("Email sent!")
    except Exception as e:
        print(f"Email error: {e}")

def get_latest_tweet():
    for url in NITTER_INSTANCES:
        try:
            r = requests.get(url, timeout=5,
                headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', r.text)
                if titles and len(titles) > 1:
                    return titles[1]
        except:
            continue
    return None

print("Watching 1337 Twitter every 5 seconds...")
while True:
    tweet = get_latest_tweet()
    if tweet and tweet != last_tweet:
        if last_tweet != "":
            print(f"NEW TWEET: {tweet}")
            send_alert(tweet)
        else:
            print(f"Started. Latest tweet: {tweet}")
        last_tweet = tweet
    else:
        print("No new tweet...")
    time.sleep(5)
