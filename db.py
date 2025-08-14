# db.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',         # หรือ IP ของ MySQL Server
        port=3307,
        user='root',              # ใส่ user ที่ใช้เชื่อมต่อ
        password='', # ใส่รหัสผ่าน
        database='tire_shop'   # ชื่อฐานข้อมูลของคุณ
      #  charset='utf8mb4'
    )
# handlers/db_queries.py
from db import get_connection