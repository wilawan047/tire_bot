import os
from dotenv import load_dotenv

# โหลด environment variables จาก .env ถ้ามี
load_dotenv()

# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # โหลด .env ถ้าอยู่ local

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "mysql.railway.internal"),
    "port": int(os.environ.get("DB_PORT", 21922)),  # ต้องใช้ port จริงจาก Railway
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_DATABASE", "railway"),
}


print("Connecting to MySQL:", DB_CONFIG)

# LINE Bot Token & Secret
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

# URL ของเว็บ (ใช้สำหรับสร้าง URL รูปภาพ)
BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")
