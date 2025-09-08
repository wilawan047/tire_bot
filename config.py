import os
from dotenv import load_dotenv

# โหลด environment variables จาก .env ถ้ามี
load_dotenv()

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": int(os.environ["DB_PORT"]),
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ["DB_NAME"],
}

# LINE Bot Token & Secret
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

# URL ของเว็บ (ใช้สำหรับสร้าง URL รูปภาพ)
BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")
