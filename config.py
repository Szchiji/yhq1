import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "你的机器人TOKEN")
DOMAIN = os.getenv("DOMAIN", "https://你的域名")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = DOMAIN + WEBHOOK_PATH
