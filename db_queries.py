import mysql.connector
from config import DB_CONFIG

# ลบบรรทัด 'from datetime import date' ออก
# db_queries.py
def get_db_connection():
    """สร้างและส่งคืนการเชื่อมต่อกับฐานข้อมูล MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# --- ฟังก์ชันสำหรับจัดการยางรถยนต์ (ไม่เปลี่ยนแปลง) ---
def get_all_tire_brands():
    """ดึงยี่ห้อยางทั้งหมด"""
    conn = get_db_connection()
    if not conn: return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT brand_id, brand_name FROM brands")
        return cur.fetchall()
    except mysql.connector.Error as err:
        print(f"Error getting tire brands: {err}")
        return []
    finally: conn.close()

def get_tire_models_by_brand_id(brand_id):
    """ดึงรุ่นยางตาม brand_id"""
    conn = get_db_connection()
    if not conn: return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT model_id, model_name FROM tire_models WHERE brand_id = %s", (brand_id,))
        return cur.fetchall()
    except mysql.connector.Error as err:
        print(f"Error getting tire models: {err}")
        return []
    finally: conn.close()

def get_tire_model_by_name(model_name):
    """ดึงข้อมูลรุ่นยางตามชื่อ"""
    conn = get_db_connection()
    if not conn: return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT model_id, model_name FROM tire_models WHERE LOWER(model_name) = LOWER(%s)", (model_name,))
        return cur.fetchone()
    except mysql.connector.Error as err:
        print(f"Error getting tire model by name: {err}")
        return None
    finally: conn.close()

def get_tires_by_model_id(model_id):
    """ดึงข้อมูลยางทั้งหมดของรุ่นที่ระบุ"""
    conn = get_db_connection()
    if not conn: return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT tire_id, model_id, full_size, load_index, speed_symbol, ply_rating, price_each, price_set, promotion_price, tire_image_url
            FROM tires
            WHERE model_id = %s
        """, (model_id,))
        return cur.fetchall()
    except mysql.connector.Error as err:
        print(f"Error getting tires by model ID: {err}")
        return []
    finally: conn.close()

# --- ฟังก์ชันสำหรับจัดการโปรโมชั่นและบริการ (ส่วนที่แก้ไข) ---
def get_active_promotions():
    """ดึงโปรโมชั่นที่ใช้งานอยู่ทั้งหมด"""
    conn = get_db_connection()
    if not conn: return []
    try:
        cur = conn.cursor(dictionary=True)
        # 🟢 โค้ดที่แก้ไขแล้ว: ดึงโปรโมชันทั้งหมดโดยไม่มีเงื่อนไขวันที่
        cur.execute("""
            SELECT promotion_id, title, description, image_url, start_date, end_date 
            FROM promotions
            ORDER BY start_date DESC
        """)
        return cur.fetchall()
    except mysql.connector.Error as err:
        print(f"Error getting promotions: {err}")
        return []
    finally: conn.close()



def get_services_by_category(category_name):
    """ดึงบริการทั้งหมดในหมวดหมู่ที่ระบุ."""
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT service_id, category, service_name FROM services ORDER BY service_id")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error getting all services: {err}")
        return []
    finally:
        conn.close()
