import os
import mysql.connector

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
