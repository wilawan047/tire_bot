import os
from dotenv import load_dotenv

load_dotenv()  # โหลดจาก .env ถ้า run local

DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "mysql.railway.internal"),
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": os.environ.get("MYSQL_DATABASE", "railway"),
}

print("Connecting to MySQL:", DB_CONFIG)

# LINE Bot Token & Secret
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

# URL ของเว็บ (ใช้สำหรับสร้าง URL รูปภาพ)
BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")
