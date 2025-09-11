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
        cur.execute("""
            SELECT tm.model_id, tm.model_name, tm.tire_category, b.brand_name
            FROM tire_models tm
            LEFT JOIN brands b ON tm.brand_id = b.brand_id
            WHERE LOWER(tm.model_name) = LOWER(%s)
        """, (model_name,))
        result = cur.fetchone()
        print(f"Debug - get_tire_model_by_name: Found model '{model_name}' -> {result}")
        return result
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
        result = cur.fetchall()
        print(f"Debug - get_tires_by_model_id: Found {len(result)} tires for model_id {model_id}")
        
        # แสดงข้อมูลตามที่มีจริงในฐานข้อมูล ไม่เพิ่มเติม
        
        return result
    except mysql.connector.Error as err:
        print(f"Error getting tires by model ID: {err}")
        return []
    finally: conn.close()


def get_tires_by_model_name(model_name):
    """ดึงข้อมูลยางทั้งหมดของรุ่นที่ระบุโดยใช้ชื่อรุ่น"""
    conn = get_db_connection()
    if not conn: return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT t.tire_id, t.model_id, t.full_size, t.load_index, t.speed_symbol, t.ply_rating, 
                   t.price_each, t.price_set, t.promotion_price, t.tire_image_url
            FROM tires t
            LEFT JOIN tire_models tm ON t.model_id = tm.model_id
            WHERE tm.model_name = %s
        """, (model_name,))
        result = cur.fetchall()
        
        print(f"Debug - get_tires_by_model_name: Found {len(result)} tires for '{model_name}'")
        
        # ถ้าไม่พบข้อมูล ให้ลองค้นหาด้วยชื่อรุ่นที่คล้ายกัน
        if not result and model_name.upper() == "EXM2+":
            print("Debug - Trying fallback for EXM2+ with model_id = 1")
            # สำหรับ EXM2+ ให้ดึงข้อมูลยางที่ใช้ model_id = 1
            cur.execute("""
                SELECT tire_id, model_id, full_size, load_index, speed_symbol, ply_rating, 
                       price_each, price_set, promotion_price, tire_image_url
                FROM tires
                WHERE model_id = 1
            """)
            result = cur.fetchall()
            print(f"Debug - Fallback found {len(result)} tires for EXM2+")
        elif not result and model_name.upper() == "ENERGY XM2+":
            print("Debug - Trying fallback for ENERGY XM2+ with model_id = 2")
            # สำหรับ ENERGY XM2+ ให้ดึงข้อมูลยางที่ใช้ model_id = 2
            cur.execute("""
                SELECT tire_id, model_id, full_size, load_index, speed_symbol, ply_rating, 
                       price_each, price_set, promotion_price, tire_image_url
                FROM tires
                WHERE model_id = 2
            """)
            result = cur.fetchall()
            print(f"Debug - Fallback found {len(result)} tires for ENERGY XM2+")
        elif not result and model_name.upper() == "PRIMACRY SUV+":
            print("Debug - Trying fallback for PRIMACRY SUV+ with model_id = 5")
            # สำหรับ PRIMACRY SUV+ ให้ดึงข้อมูลยางที่ใช้ model_id = 5
            cur.execute("""
                SELECT tire_id, model_id, full_size, load_index, speed_symbol, ply_rating, 
                       price_each, price_set, promotion_price, tire_image_url
                FROM tires
                WHERE model_id = 5
            """)
            result = cur.fetchall()
            print(f"Debug - Fallback found {len(result)} tires for PRIMACRY SUV+")
            
            # แสดงข้อมูลตามที่มีจริงในฐานข้อมูล ไม่เพิ่มเติม
        
        return result
    except mysql.connector.Error as err:
        print(f"Error getting tires by model name: {err}")
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

def get_all_service_categories():
    """ดึงหมวดหมู่บริการทั้งหมดจากตาราง services."""
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT category FROM services")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error getting service categories: {err}")
        return []
    finally: conn.close()
def get_services_by_category(category_name):
    """ดึงบริการทั้งหมดในหมวดหมู่ที่ระบุ."""
    print(f"Debug - get_services_by_category called with: '{category_name}'")
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.service_id, s.category, s.service_name, 
                   GROUP_CONCAT(so.option_name SEPARATOR ', ') as options
            FROM services s
            LEFT JOIN service_options so ON s.service_id = so.service_id
            WHERE s.category = %s
            GROUP BY s.service_id, s.category, s.service_name
            ORDER BY s.service_id
        """, (category_name,))
        result = cursor.fetchall()
        print(f"Debug - Found {len(result)} services for category '{category_name}'")
        return result
    except mysql.connector.Error as err:
        print(f"Error getting services by category: {err}")
        return []
    finally: conn.close()


def get_models_by_brand(brand_name):
    """ดึงข้อมูลรุ่นยางทั้งหมดของแบรนด์ที่ระบุ"""
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT tm.model_id, tm.model_name, tm.tire_category, b.brand_name
            FROM tire_models tm
            LEFT JOIN brands b ON tm.brand_id = b.brand_id
            WHERE b.brand_name = %s
            ORDER BY tm.model_name
        """, (brand_name,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error getting models by brand: {err}")
        return []
    finally: conn.close()


def get_tire_model_image(model_name):
    """ดึงรูปภาพของรุ่นยางจากฐานข้อมูล"""
    conn = get_db_connection()
    if not conn: return "https://placeholder.vercel.app/images/default-tire.jpg"
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.tire_image_url
            FROM tires t
            LEFT JOIN tire_models tm ON t.model_id = tm.model_id
            WHERE tm.model_name = %s
            LIMIT 1
        """, (model_name,))
        result = cursor.fetchone()
        
        if result and result.get("tire_image_url"):
            # สร้าง URL รูปภาพโดยตรง
            image_url = result["tire_image_url"]
            if image_url.startswith("http"):
                return image_url
            else:
                # แก้ไขชื่อไฟล์รูปภาพให้ถูกต้องตามรุ่นยาง
                if model_name.upper() == "EXM2+":
                    # ใช้รูปภาพที่เหมาะสมสำหรับ EXM2+
                    return "https://webtire-production.up.railway.app/static/uploads/tires/Michelin_ENERGY_XM2_+_EXM2+.png"
                elif model_name.upper() == "ENERGY XM2+":
                    # ใช้รูปภาพที่เหมาะสมสำหรับ ENERGY XM2+
                    return "https://webtire-production.up.railway.app/static/uploads/tires/Michelin_ENERGY_XM2_+_EXM2+.png"
                else:
                    return f"https://webtire-production.up.railway.app/static/uploads/tires/{image_url}"
        else:
            return "https://placeholder.vercel.app/images/default-tire.jpg"
    except mysql.connector.Error as err:
        print(f"Error getting tire model image: {err}")
        return "https://placeholder.vercel.app/images/default-tire.jpg"
    finally: conn.close()

def get_tire_model_name_by_id(model_id):
    """ดึงชื่อรุ่นยางตาม model_id"""
    conn = get_db_connection()
    if not conn: return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT tm.model_id, tm.model_name, tm.tire_category, b.brand_name
            FROM tire_models tm
            LEFT JOIN brands b ON tm.brand_id = b.brand_id
            WHERE tm.model_id = %s
        """, (model_id,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Error getting tire model by ID: {err}")
        return None
    finally: conn.close()
