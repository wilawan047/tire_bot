# config.py
import os
from dotenv import load_dotenv
load_dotenv()


# ข้อมูลการเชื่อมต่อฐานข้อมูล
DB_CONFIG = {
   "host": os.environ.get("MYSQL_HOST", "mysql.railway.internal"),
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", "fzqPryLRlGdCOLAVZeXoxmikHelGJPBk"),
    "database": os.environ.get("MYSQL_DATABASE", "railway")
}

# Line Bot API
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
MAKE_WEBHOOK_URL = os.environ.get("MAKE_WEBHOOK_URL")

# ChatPDF API Key
CHATPDF_API_KEY = os.environ.get("CHATPDF_API_KEY")