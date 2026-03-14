asyncio

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
MARKER = "Any available Check-ins will appear here"
URL = "https://admission.1337.ma"

async def alert():
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID,
        text="🚨 1337 SLOT OPEN!\n\nGO NOW 👉 https://admission.1337.ma")

print("✅ Watching 1337...")
while True:
    try:
        r = requests.get(URL, timeout=10, headers={"User-Agent":"Mozilla/5.0"})
        if MARKER not in r.text:
            asyncio.run(alert())
