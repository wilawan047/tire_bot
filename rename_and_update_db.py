import os
import mysql.connector
from urllib.parse import quote

# -----------------------------
# 1. ตั้งค่า Database ของ Railway
# -----------------------------
db_config = {
    "host": "ballast.proxy.rlwy.net",
    "user": "root",
    "password": "fzqPryLRlGdCOLAVZeXoxmikHelGJPBk",
    "database": "tire_shop"  # ชื่อฐานข้อมูลของคุณ
}

# เชื่อมต่อ DB
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# -----------------------------
# 2. โฟลเดอร์ไฟล์รูป
# -----------------------------
folder = "static/images"

# -----------------------------
# 3. Loop rename + update DB
# -----------------------------
for filename in os.listdir(folder):
    name, ext = os.path.splitext(filename)

    # สร้างชื่อใหม่
    new_name = name.replace(" ", "_").replace("+", "") + ext

    # Rename ไฟล์ถ้ายังไม่ได้ rename
    if filename != new_name:
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")

        # Update ชื่อไฟล์ใน DB
        sql = "UPDATE tires SET filename=%s WHERE filename=%s"
        cursor.execute(sql, (new_name, filename))
        print(f"Updated DB: {filename} -> {new_name}")

# Commit การเปลี่ยนแปลงใน DB
conn.commit()

# ปิดการเชื่อมต่อ
cursor.close()
conn.close()

print("All files renamed and DB updated!")

def get_image_url(filename):
    base_url = os.environ.get("BASE_URL", "").rstrip("/")
    resolved = resolve_image_filename(filename) if filename else None
    if not resolved:
        return "https://via.placeholder.com/400x300?text=No+Image"
    filename = resolved

    # เพิ่ม query string ป้องกัน cache
    import time
    version = int(time.time())
    url_path = f"/static/uploads/tires/{quote(filename)}?v={version}"
    if base_url:
        url = f"{base_url}{url_path}"
    else:
        url = url_path
    print("URL ที่ถูกสร้าง:", url)
    return url

def resolve_image_filename(filename):
    """
    ตรวจสอบว่าไฟล์นี้มีอยู่ในโฟลเดอร์หรือไม่
    ถ้าไม่มี ให้ลองแปลงชื่อ (เช่น แทนที่ space, lowercase ฯลฯ)
    ถ้ายังไม่เจอ ให้ return None
    """
    import os

    folder = "static/images"  # หรือ static/uploads/tires ตามที่ใช้จริง
    if not filename:
        return None

    # ตรวจสอบชื่อไฟล์ตรงๆ
    path = os.path.join(folder, filename)
    if os.path.isfile(path):
        return filename

    # ลองแปลงชื่อ (เช่น แทนที่ space ด้วย _, lowercase)
    alt_name = filename.replace(" ", "_").lower()
    alt_path = os.path.join(folder, alt_name)
    if os.path.isfile(alt_path):
        return alt_name

    # หาไฟล์ที่ชื่อคล้ายกัน (เช่น เฉพาะชื่อ ไม่สนใจนามสกุล)
    name, ext = os.path.splitext(filename)
    for f in os.listdir(folder):
        if f.lower().startswith(name.lower()):
            return f

    # ไม่พบไฟล์
    return None
