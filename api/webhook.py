from flask import Flask, request, abort, jsonify, send_from_directory
import mysql.connector
import os
import sys
import config
from flask import url_for
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from make_integration import forward_to_make
from chatpdf_integration import forward_to_chatpdf
from werkzeug.utils import secure_filename
from urllib.parse import quote
from flask import send_from_directory
from urllib.parse import quote
import re
from db_queries import (
    get_active_promotions,
    get_all_tire_brands, get_tire_models_by_brand_id,
    get_tire_model_by_name, get_tires_by_model_id,
    get_all_service_categories, get_services_by_category
)
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction,
    FlexSendMessage, LocationSendMessage, StickerMessage
)
import config
LINE_CHANNEL_ACCESS_TOKEN = config.LINE_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET = config.LINE_CHANNEL_SECRET

app = Flask(__name__, static_folder="static")


line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")


user_pages = {}
@app.route("/api/webhook", methods=["POST"])
def callback():
    body = request.get_data(as_text=True)  # รับเป็น string
    signature = request.headers.get("X-Line-Signature")
    print("Signature:", signature)
   
    if not signature:
        return "Missing signature", 400
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ Invalid signature")
        return "Invalid signature", 401
    except Exception as e:
        print("Error:", e)
        return "Error", 500
    return "OK", 200




import os
from flask import send_from_directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, 'static', 'images2')

# Route สำหรับ serve static images (เพื่อให้ LINE Flex หรือ browser เข้าถึงได้)
@app.route('/static/images2/<path:filename>')
def custom_static(filename):
    print("Serving:", os.path.join(IMAGE_DIR, filename))
    return send_from_directory(IMAGE_DIR, filename)

@app.route("/", methods=["GET", "POST"])
def home():
    return "LINE Bot Webhook is running!", 200


# ฟังก์ชันตรวจสอบว่าไฟล์มีจริงใน static/images2
def file_exists(filename):
    if not filename:
        return False
    return os.path.isfile(os.path.join("static/images2", filename))

# ฟังก์ชันสร้าง URL ของรูปพร้อม fallback
def get_image_url(filename):
    base_url = os.environ.get("BASE_URL", "").rstrip("/")
    
    # กรณีไฟล์ไม่กำหนดหรือไม่เจอใน static/images2
    if not filename or not file_exists(filename):
        print(f"❌ File missing: {filename}, ใช้ fallback image")
        # สามารถใช้รูป placeholder online หรือ default ใน static
        fallback_file = "default-tire.jpg"
        # ตรวจสอบ fallback file
        if not file_exists(fallback_file):
            return "https://via.placeholder.com/400x300?text=No+Image"
        filename = fallback_file

    # ถ้า BASE_URL ว่าง ให้ใช้ path relative ของ Flask (local testing)
    if not base_url:
        url = f"/static/images2/{quote(filename)}"
    else:
        url = f"{base_url}/static/images2/{quote(filename)}"
    
    print("URL ที่ถูกสร้าง:", url)
    return url




def build_quick_reply_buttons(buttons):
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label=label, text=text))
        for label, text in buttons
    ])

def build_tire_flex(tire, model_name):
    image_url = get_image_url(tire.get("tire_image_url"))
    return {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectRatio": "4:3",
            "aspectMode": "fit"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": model_name or "ไม่ทราบรุ่น", "weight": "bold", "size": "lg", "wrap": True},
                {"type": "separator", "margin": "md"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "spacing": "sm",
                    "contents": [
                        {"type": "text", "text": f"ขนาด: {tire.get('full_size') or '-'}"},
                        {"type": "text", "text": f"Load Index: {tire.get('load_index') or '-'}"},
                        {"type": "text", "text": f"Speed Symbol: {tire.get('speed_symbol') or '-'}"},
                        {"type": "text", "text": f"Ply Rating: {tire.get('ply_rating') or '-'}"},
                        {"type": "text", "text": f"💰 ราคา/เส้น: {tire.get('price_each') or '-'} บาท"},
                        {"type": "text", "text": f"💰 ราคา/ชุด: {tire.get('price_set') or '-'} บาท"},
                        {"type": "text", "text": f"🔥 โปรพิเศษ: {tire.get('promotion_price') or '-'} บาท"}
                    ]
                }
            ]
        }
    }

def build_service_list_flex(category_name, services):
    """สร้าง Flex Message แสดงรายการบริการแบบง่ายๆ"""
    
    # สร้างรายการบริการ
    service_items = []
    for service in services:
        # สร้างรายการตัวเลือกบริการ
        options_text = service.get('options', '')
        service_contents = [
            {
                "type": "text",
                "text": service.get('service_name', 'ไม่ระบุ'),
                "size": "sm",
                "weight": "bold",
                "wrap": True
            }
        ]
        
        # เพิ่มตัวเลือกถ้ามี
        if options_text:
            service_contents.append({
                "type": "text",
                "text": f"ตัวเลือก: {options_text}",
                "size": "xs",
                "color": "#666666",
                "wrap": True
            })
        
        service_item = {
            "type": "box",
            "layout": "horizontal",
            "margin": "sm",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": "🔧",
                    "size": "sm",
                    "flex": 0
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "flex": 1,
                    "contents": service_contents
                }
            ]
        }
        service_items.append(service_item)
    
    # สร้าง Flex Message
    return {
        "type": "bubble",
        "size": "giga",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"🛠️ {category_name.upper()}",
                    "weight": "bold",
                    "size": "lg",
                    "color": "#FFFFFF"
                }
            ],
            "backgroundColor": "#3EEF68DA",
            "paddingAll": "md"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": service_items
        }
    }

import mysql.connector

def get_tire_model_name_by_id(model_id):
    try:
        conn = mysql.connector.connect(**config.DB_CONFIG) # แก้ไขตรงนี้
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT model_name FROM tire_models WHERE model_id = %s", (model_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result
        else:
            return {"model_name": "Unknown Model"}
    except Exception as e:
        print(f"Error in get_tire_model_name_by_id: {e}")
        return {"model_name": "Unknown Model"}
    
def build_promotion_flex(promo):
    image_url = get_image_url(promo.get('image_url')) # ดึง URL แบบเต็มจากฐานข้อมูล
    
    # เพิ่มการตรวจสอบเพื่อความปลอดภัย
    if not image_url or "http" not in image_url:
        image_url = "https://placeholder.vercel.app/images/default-promotion.jpg"
    
    return {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": image_url, # ใช้ URL แบบเต็มที่ดึงมา
            "size": "full",
            "aspectRatio": "4:3",
            "aspectMode": "fit"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": promo.get("title", "-"), "weight": "bold", "size": "lg", "wrap": True},
                {"type": "text", "text": promo.get("description", "-"), "size": "sm", "wrap": True, "margin": "md"},
                {"type": "text", "text": f"📅 {promo['start_date']} ถึง {promo['end_date']}", "size": "xs", "color": "#888888", "margin": "md"}
            ]
        }
    }

def send_tires_page(reply_token, user_id):
    if user_id not in user_pages:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="กรุณาเลือกยี่ห้อและรุ่นก่อน"))
        return
    page_size = 10
    page = user_pages[user_id]['page']
    model_id = user_pages[user_id]['model_id']

    tires = get_tires_by_model_id(model_id)
    if not tires:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="ไม่พบข้อมูลยาง"))
        return

    start = (page - 1) * page_size
    end = start + page_size
    tires_page = tires[start:end]

    tire_model = get_tire_model_name_by_id(model_id)
    model_name = tire_model.get('model_name', "Unknown Model")

    bubbles = [build_tire_flex(t, model_name) for t in tires_page]
    carousel = {"type": "carousel", "contents": bubbles}
    flex_msg = FlexSendMessage(alt_text=f"ข้อมูลยางรุ่นหน้า {page}", contents=carousel)

    nav_buttons = []
    if page > 1:
        nav_buttons.append(("⬅️ ก่อนหน้า", f"page_{page - 1}"))
    if end < len(tires):
        nav_buttons.append(("ถัดไป ➡️", f"page_{page + 1}"))

    nav_buttons.extend([
        ("↩️ เลือกรุ่นอื่น", "ยี่ห้อยางรถยนต์"),
        ("🏠 เมนูหลัก", "แนะนำ"),
    ])

    line_bot_api.reply_message(reply_token, [
        flex_msg,
        TextSendMessage(text="👇 เมนูเพิ่มเติม", quick_reply=build_quick_reply_buttons(nav_buttons))
    ])
# ======================
# 🔍 ค้นหายี่ห้อจากข้อความ
# ======================
def find_brand_in_text(text):
    text_lower = text.lower()
    brands = get_all_tire_brands()
    for b in brands:
        if b['brand_name'].lower() in text_lower:
            return b
    return None

# ======================
# 🔍 ค้นหารุ่นจากข้อความ
# ======================
def find_model_in_text(text):
    text_lower = text.lower()
    all_brands = get_all_tire_brands()
    for b in all_brands:
        models = get_tire_models_by_brand_id(b['brand_id'])
        for m in models:
            if m['model_name'].lower() in text_lower:
                return m
    return None




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()
    reply_token = event.reply_token
    user_id = event.source.user_id

    try:
        # 1️⃣ ทักทาย
        if any(word in text.lower() for word in ["สวัสดี", "hello", "hi", "หวัดดี"]):
            line_bot_api.reply_message(reply_token, TextSendMessage(
                text="สวัสดีค่ะ 😊 ยินดีต้อนรับสู่ร้านยางของเราค่ะ\nต้องการให้เราช่วยแนะนำยาง หรือสอบถามบริการอื่น ๆ ไหมคะ 👇",
                quick_reply=build_quick_reply_buttons([
                    ("🚗 แนะนำยาง", "แนะนำ"),
                    ("🛠️ บริการ", "บริการ"),
                    ("🎉 โปรโมชัน", "โปรโมชัน"),
                    ("📍 ร้านอยู่ที่ไหน", "ร้านอยู่ไหน"),
                    ("📞 ติดต่อร้าน", "ติดต่อร้าน")
                ])
            ))
        
        # 2️⃣ เมนูหลัก
        elif text in ["แนะนำ", "แนะนำยาง", "ยาง", "แนะนำหน่อย","แนะนำยางรถยนต์", "เริ่มต้นเลือกยาง"]:
            line_bot_api.reply_message(reply_token, TextSendMessage(
                text="เลือกเมนูที่ต้องการ👇",
                quick_reply=build_quick_reply_buttons([
                    ("🚗 ยี่ห้อยางรถยนต์", "ยี่ห้อยางรถยนต์"),
                    ("🛠️ บริการ", "บริการ"),
                    ("🎉 โปรโมชัน", "โปรโมชัน"),
                    ("📞 ติดต่อร้าน", "ติดต่อร้าน"),
                    ("🕗 เวลาเปิดทำการ", "เวลาเปิดทำการ")
                ])
            ))


        # 3️⃣ ขอเลือกยี่ห้อ
        elif text == "ยี่ห้อยางรถยนต์":
            brands = get_all_tire_brands()
            if not brands:
                line_bot_api.reply_message(reply_token, TextSendMessage(text="ไม่พบยี่ห้อยาง"))
            else:
                line_bot_api.reply_message(reply_token, TextSendMessage(
                    text="เลือกยี่ห้อที่คุณต้องการ 🔽",
                    quick_reply=build_quick_reply_buttons([
                        (b['brand_name'], b['brand_name']) for b in brands[:10]
                    ])
                ))

        # 4️⃣ แสดงรายการยี่ห้อทั้งหมด
        elif "ยางแบนด์อะไรบ้าง" in text or "ยี่ห้ออะไรบ้าง" in text or "มียางยี่ห้ออะไร" in text:
            brands = get_all_tire_brands()
            if brands:
                brand_list = "\n".join([f"- {b['brand_name']}" for b in brands])
                line_bot_api.reply_message(reply_token, TextSendMessage(
                    text=f"📌 ยี่ห้อที่มีในร้าน:\n{brand_list}"
                ))
            else:
                line_bot_api.reply_message(reply_token, TextSendMessage(
                    text="ไม่พบข้อมูลยี่ห้อยางในระบบ"
                ))

        # 5️⃣ แสดงรุ่นทั้งหมด
        elif "รุ่นอะไรบ้าง" in text or "มียางรุ่นอะไร" in text:
            brands = get_all_tire_brands()
            all_models = []
            for b in brands:
                models = get_tire_models_by_brand_id(b['brand_id'])
                if models:
                    model_names = ", ".join([m['model_name'] for m in models])
                    all_models.append(f"{b['brand_name']}: {model_names}")
            if all_models:
                reply_text = "📌 รุ่นยางที่มีในร้าน:\n" + "\n".join(all_models)
                line_bot_api.reply_message(reply_token, TextSendMessage(text=reply_text))
            else:
                line_bot_api.reply_message(reply_token, TextSendMessage(
                    text="ไม่พบข้อมูลรุ่นยางในระบบ"
                ))

        # 6️⃣ ตรวจสอบชื่อยี่ห้อ → แสดงรุ่น
        elif (brand := find_brand_in_text(text)):
            models = get_tire_models_by_brand_id(brand['brand_id'])
            if models:
                line_bot_api.reply_message(reply_token, TextSendMessage(
                    text=f"กรุณาเลือกรุ่นยางของ {brand['brand_name']} 🔽",
                    quick_reply=build_quick_reply_buttons([
                        (m['model_name'], m['model_name']) for m in models[:13]
                    ])
                ))
            else:
                line_bot_api.reply_message(reply_token, TextSendMessage(
                    text=f"ไม่พบรุ่นของยี่ห้อ {brand['brand_name']} ในระบบ"
                ))


        # 7️⃣ ตรวจสอบชื่อรุ่น → แสดง Flex
        elif (model := get_tire_model_by_name(text)) or (model := find_model_in_text(text)):
            tires = get_tires_by_model_id(model['model_id'])
            if tires:
                user_pages[user_id] = {'model_id': model['model_id'], 'page': 1}
                send_tires_page(reply_token, user_id)
            else:
                line_bot_api.reply_message(reply_token, TextSendMessage(
                    text=f"ขออภัย ไม่พบข้อมูลยางสำหรับรุ่น {model['model_name']} ในระบบ"
                ))

        # 8️⃣ พิกัดร้าน
        elif any(w in text for w in ["ร้านอยู่ไหน", "แผนที่", "location", "พิกัด", "ที่อยู่ร้าน", "โลเคชัน", "ที่ตั้งร้าน", "ร้านอยู่ที่ไหน","แผนที่ร้าน"]):
            line_bot_api.reply_message(reply_token, LocationSendMessage(
                title="ไทร์พลัส บุรีรัมย์แสงเจริญการยาง",
                address="365 หมู่ 3 ถนน จิระ ต.ในเมือง อ.เมือง จ.บุรีรัมย์ 31000",
                latitude=14.9977752,
                longitude=103.0387382
            ))


        # 9️⃣ ติดต่อ / เวลา
        elif text in ["ติดต่อ", "ติดต่อร้าน", "ติดต่อร้านยาง", "ติดต่อเรา", "เบอร์โทร", "โทรศัพท์"]:
            line_bot_api.reply_message(reply_token, TextSendMessage(text="ติดต่อเราได้ที่ ☎️ 044 611 097"))


        elif any(word in text.lower() for word in ["เวลาเปิดทำการ", "เปิด", "ร้านเปิดกี่โมง", "ร้านเปิด"]):
            line_bot_api.reply_message(reply_token, TextSendMessage(
                text="เวลาเปิดทำการ 🕗 วันจันทร์ - วันเสาร์ : 08:00 - 17:30"
            ))


        # 🔟 โปรโมชัน
        elif text in ["โปรโมชัน", "โปรโมชั่น", "โปร"]:
            promotions = get_active_promotions()
            if not promotions:
                line_bot_api.reply_message(reply_token, TextSendMessage(text="ขณะนี้ยังไม่มีโปรโมชันค่ะ"))
            else:
                bubbles = [build_promotion_flex(p) for p in promotions[:10]]
                carousel = {"type": "carousel", "contents": bubbles}
                flex_msg = FlexSendMessage(alt_text="โปรโมชันล่าสุด", contents=carousel)
                quick_buttons = [("🏠 เมนูหลัก", "แนะนำ")]
                quick_reply_msg = TextSendMessage(text="👇", quick_reply=build_quick_reply_buttons(quick_buttons))
                line_bot_api.reply_message(reply_token, [flex_msg, quick_reply_msg])

        # 1️⃣1️⃣ แสดงหมวดหมู่บริการ
        elif text in ["บริการ", "service", "บริการทั้งหมด"]:
            categories = get_all_service_categories()
            if not categories:
                line_bot_api.reply_message(reply_token, TextSendMessage(text="ยังไม่มีข้อมูลบริการในระบบค่ะ"))
            else:
                quick_buttons = [("🏠 เมนูหลัก", "แนะนำ")]
                quick_buttons.extend([(cat['category'], f"หมวดบริการ:{cat['category']}") for cat in categories])
                line_bot_api.reply_message(reply_token, TextSendMessage(
                    text="กรุณาเลือกหมวดหมู่บริการ 🔽",
                    quick_reply=build_quick_reply_buttons(quick_buttons)
                ))

        # 1️⃣2️⃣ แสดงบริการในหมวดหมู่
        elif text.startswith("หมวดบริการ:"):
            category_name = text.split(":", 1)[1]
            services = get_services_by_category(category_name)
            if not services:
                line_bot_api.reply_message(reply_token, TextSendMessage(text=f"ไม่มีบริการในหมวดหมู่ {category_name}"))
            else:
                flex_content = build_service_list_flex(category_name, services)
                flex_msg = FlexSendMessage(alt_text=f"บริการ {category_name}", contents=flex_content)
                quick_buttons = [
                    ("🏠 เมนูหลัก", "แนะนำ"), 
                    ("↩️ ย้อนกลับ", "บริการ"),
                    ("📋 ดูหมวดอื่น", "บริการ")
                ]
                quick_reply_msg = TextSendMessage(
                    text="หากท่านต้องการทำการจองเพื่อเข้าใช้บริการสามารถกดดูรายละเอียดบริการได้ที่ rich menu ครับ 📌",
                    quick_reply=build_quick_reply_buttons(quick_buttons)
                )
                line_bot_api.reply_message(reply_token, [flex_msg, quick_reply_msg])

        # 1️⃣3️⃣ ไม่เข้าเงื่อนไข → ส่งไป ChatPDF → Make
        else:
            raise Exception("ไม่เข้าใจคำสั่ง")

    except Exception as e:
        print("❗️ไม่เข้าเงื่อนไข → ส่งไปถาม ChatPDF:", e)
        try:
            answer = forward_to_chatpdf({
                "replyToken": reply_token,
                "userId": user_id,
                "text": text
            })
            line_bot_api.reply_message(reply_token, TextSendMessage(text=answer))
        except Exception as chatpdf_err:
            print("❌ ChatPDF error → fallback ไป Make:", chatpdf_err)
            try:
                forward_to_make({
                    "replyToken": reply_token,
                    "userId": user_id,
                    "text": text
                })
            except Exception as make_err:
                print("❌ Make ก็ล้มเหลว:", make_err)
                line_bot_api.reply_message(reply_token, TextSendMessage(
                    text="ขออภัย ไม่สามารถตอบคำถามของคุณได้ในขณะนี้ค่ะ 😅"
                ))


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    reply_token = event.reply_token
    line_bot_api.reply_message(reply_token, TextSendMessage(
        text="ขอบคุณสำหรับสติ๊กเกอร์นะคะ 😊\nต้องการให้เราช่วยอะไรดีคะ👇",
        quick_reply=build_quick_reply_buttons([
            ("🚗 เริ่มต้นเลือกยาง", "แนะนำ"),
            ("🛠️ บริการ", "บริการ"),
            ("🎉 โปรโมชัน", "โปรโมชัน"),
            ("📍 ร้านอยู่ที่ไหน", "ร้านอยู่ไหน"),
            ("📞 ติดต่อร้าน", "ติดต่อร้าน")
        ])
    ))
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
