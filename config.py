import os
from dotenv import load_dotenv

# โหลด environment variables จาก .env ถ้ามี
load_dotenv()

# config.py
DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ.get("DB_PORT")),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_DATABASE"),  # <- แก้ตรงนี้
}

# LINE Bot Token & Secret
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

# URL ของเว็บ (ใช้สำหรับสร้าง URL รูปภาพ)
BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")
