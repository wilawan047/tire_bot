import os
import sys
import re
from urllib.parse import quote
from werkzeug.utils import secure_filename

import mysql.connector
from flask import Flask, request, abort, jsonify, send_from_directory, url_for

import config
from make_integration import forward_to_make
from chatpdf_integration import forward_to_chatpdf

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


# ฟังก์ชันเดิม
def build_quick_reply_buttons(buttons):
    return QuickReply(
        items=[QuickReplyButton(action=MessageAction(label=label, text=text)) for label, text in buttons]
    )


def build_quick_reply_with_extra(buttons):
    """เพิ่มปุ่ม ❓ ถามคำถามอื่น ให้ทุกเมนูอัตโนมัติ และย้ายมาไว้หน้าสุด"""
    extra_button = ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
    if extra_button not in buttons:
        buttons.insert(0, extra_button)
    return QuickReply(
        items=[QuickReplyButton(action=MessageAction(label=label, text=text))
               for label, text in buttons]
    )


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
        service_contents = [
            {
                "type": "text",
                "text": service.get('service_name', 'ไม่ระบุ'),
                "size": "sm",
                "weight": "bold",
                "wrap": True
            }
        ]
        
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
            "backgroundColor": "#1EC445C5",
            "paddingAll": "md"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": service_items
        }
    }



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
            "url": image_url, 
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

def send_tires_page(reply_token, user_id, back_to="รุ่น"):
    if user_id not in user_pages:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="กรุณาเลือกยี่ห้อและรุ่นก่อน"))
        return

    page_size = 10  # LINE carousel รองรับ bubble สูงสุด 10
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
    flex_msg = FlexSendMessage(
        alt_text=f"ข้อมูลยางหน้า {page}",
        contents=carousel
    )

    # Navigation buttons
    nav_buttons = []
    if page > 1:
        nav_buttons.append(("⬅️ ก่อนหน้า", f"page_{page - 1}"))
    if end < len(tires):
        nav_buttons.append(("ถัดไป ➡️", f"page_{page + 1}"))

    nav_buttons.extend([
        (f"↩️ เลือก{back_to}อื่น", "ยี่ห้อยางรถยนต์"),
        ("🏠 เมนูหลัก", "แนะนำ"),
    ])

    line_bot_api.reply_message(
        reply_token, 
        [
            flex_msg,
            TextSendMessage(
                text="คลิกเพื่อเลือกเมนูเพิ่มเติม",
                quick_reply=build_quick_reply_with_extra(nav_buttons)
            )
        ]
    )


def find_brand_in_text(text):
    text_lower = text.lower()
    brands = get_all_tire_brands()
    for b in brands:
        if b['brand_name'].lower() in text_lower:
            return b
    return None


def find_model_in_text(text):
    text_lower = text.lower()
    all_brands = get_all_tire_brands()
    for b in all_brands:
        models = get_tire_models_by_brand_id(b['brand_id'])
        for m in models:
            if m['model_name'].lower() in text_lower:
                return m
    return None

def find_promotion_in_text(text):
    text_lower = text.lower()
    promotions = get_active_promotions()  
    for p in promotions:
        if p['title'].lower() in text_lower:
            return p
    return None

EXAMPLE_QUESTIONS = ["รุ่นยางสำหรับรถเก๋ง", "ยางสำหรับรถกระบะ"]

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()
    reply_token = event.reply_token
    user_id = event.source.user_id

    try:
        # 0️⃣ คำถามตรงกับตัวอย่าง → ส่งไป Make
        if text in EXAMPLE_QUESTIONS:
            answer_from_make = forward_to_make({
                "replyToken": reply_token,
                "userId": user_id,
                "text": text
            })

            if answer_from_make:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text=answer_from_make)
                )

        # 0.1️⃣ ถามเพิ่มเติม → แสดงตัวอย่างคำถาม
        elif text in ["ถามเพิ่มเติม", "ถามคำถามอื่น"]:
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(
                    text=(
                        "คุณสามารถพิมพ์คำถามอะไรได้เลยค่ะ เช่น:\n"
                        "- รุ่นยางสำหรับรถเก๋ง\n"
                        "- ยางสำหรับรถกระบะ\n"
                        "- โปรโมชันเดือนนี้"
                    ),
                    quick_reply=build_quick_reply_with_extra([
                        ("🏠 เมนูหลัก", "แนะนำ"),
                        ("🚗 แนะนำยาง", "แนะนำ"),
                    ])
                )
            )
            return

        # 1️⃣ ทักทาย
        elif any(word in text.lower() for word in ["สวัสดี", "hello", "hi", "หวัดดี"]):
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(
                    text=(
                        "สวัสดีค่ะ 😊 ยินดีต้อนรับสู่ร้านยางของเราค่ะ\n"
                        "ต้องการให้เราช่วยแนะนำยาง หรือสอบถามบริการอื่น ๆ ไหมคะ 👇"
                    ),
                    quick_reply=build_quick_reply_with_extra([
                        ("🚗 แนะนำยาง", "แนะนำ"),
                        ("🛠️ บริการ", "บริการ"),
                        ("🎉 โปรโมชัน", "โปรโมชัน"),
                        ("📍 ร้านอยู่ที่ไหน", "ร้านอยู่ไหน"),
                        ("📞 ติดต่อร้าน", "ติดต่อร้าน")
                    ])
                )
            )

        # 2️⃣ เมนูหลัก
        elif any(kw in text.lower() for kw in ["แนะนำ", "แนะนำยาง", "แนะนำหน่อย"]):
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(
                    text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                    quick_reply=build_quick_reply_with_extra([
                        ("🚗 ยี่ห้อยางรถยนต์", "ยี่ห้อยางรถยนต์"),
                        ("🛠️ บริการ", "บริการ"),
                        ("🎉 โปรโมชัน", "โปรโมชัน"),
                        ("📞 ติดต่อร้าน", "ติดต่อร้าน"),
                        ("🕗 เวลาเปิดทำการ", "เวลาเปิดทำการ")
                    ])
                )
            )

        # 3️⃣ ขอเลือกยี่ห้อ
        elif any(kw in text for kw in ["ยี่ห้อ", "แบนด์"]):
            brands = get_all_tire_brands()
            if brands:
                quick_buttons = [(b['brand_name'], b['brand_name']) for b in brands[:13]]
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(
                        text="📌 ยี่ห้อที่มีในร้าน:\nเลือกยี่ห้อที่คุณสนใจ 🔽",
                        quick_reply=build_quick_reply_with_extra(quick_buttons)
                    )
                )
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="ไม่พบข้อมูลยี่ห้อยางในระบบ")
                )

        # 4️⃣ แสดงรุ่น
        elif "รุ่น" in text:
            brands = get_all_tire_brands()
            all_buttons = []
            for b in brands:
                models = get_tire_models_by_brand_id(b['brand_id'])
                if models:
                    all_buttons.extend([(m['model_name'], m['model_name']) for m in models[:5]])

            if all_buttons:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(
                        text="📌 รุ่นยางที่มีในร้าน:\nเลือกรุ่นที่คุณสนใจ 🔽",
                        quick_reply=build_quick_reply_with_extra(all_buttons[:13])
                    )
                )
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="ไม่พบข้อมูลรุ่นยางในระบบ")
                )

        # 5️⃣ ตรวจสอบชื่อยี่ห้อ → แสดงรุ่น
        elif (brand := find_brand_in_text(text)):
            models = get_tire_models_by_brand_id(brand['brand_id'])
            if models:
                quick_buttons = [(m['model_name'], m['model_name']) for m in models[:13]]
                quick_buttons.append(("↩️ เลือกยี่ห้ออื่น", "ยี่ห้อยางรถยนต์"))
                quick_buttons.append(("🏠 เมนูหลัก", "แนะนำ"))

                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(
                        text=f"กรุณาเลือกรุ่นยางของ {brand['brand_name']} 🔽",
                        quick_reply=build_quick_reply_with_extra(quick_buttons)
                    )
                )

        # 6️⃣ ตรวจสอบชื่อรุ่น → แสดง Flex
        elif (model := get_tire_model_by_name(text)) or (model := find_model_in_text(text)):
            tires = get_tires_by_model_id(model['model_id'])
            if tires:
                user_pages[user_id] = {'model_id': model['model_id'], 'page': 1}
                send_tires_page(reply_token, user_id, back_to="รุ่น")
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(
                        text=f"ขออภัย ไม่พบข้อมูลยางสำหรับรุ่น {model['model_name']} ในระบบ"
                    )
                )

        # 7️⃣ จัดการข้อความ page_2, page_3 ...
        elif text.startswith("page_"):
            try:
                page_num = int(text.split("_")[1])
                if user_pages.get(user_id):
                    user_pages[user_id]['page'] = page_num
                    send_tires_page(reply_token, user_id)
                else:
                    line_bot_api.reply_message(
                        reply_token,
                        TextSendMessage(text="กรุณาเลือกยี่ห้อและรุ่นก่อนค่ะ")
                    )
            except Exception as e:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text=f"เกิดข้อผิดพลาด: {str(e)}")
                )

        # 8️⃣ โปรโมชั่น
        elif "โปรโมชัน" in text or "โปร" in text:  
            promotions = get_active_promotions()
            if promotions:
                bubbles = [build_promotion_flex(p) for p in promotions[:10]]
                flex_msg = FlexSendMessage(
                    alt_text="โปรโมชั่นปัจจุบัน",
                    contents={"type": "carousel", "contents": bubbles}
                )
                quick_buttons = [("🏠 เมนูหลัก", "แนะนำ")]
                line_bot_api.reply_message(
                    reply_token,
                    [
                        flex_msg,
                        TextSendMessage(
                            text="เลือกเมนูเพิ่มเติม",
                            quick_reply=build_quick_reply_with_extra(quick_buttons)
                        )
                    ]
                )
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="ขณะนี้ไม่มีโปรโมชั่นค่ะ 😅")
                )

        # 12️⃣ บริการ
        elif any(kw in text.lower() for kw in ["บริการ", "service", "บริการของร้าน"]):
            service_categories = get_all_service_categories()
            if service_categories:
                quick_buttons = [(cat['category'], cat['category']) for cat in service_categories[:13]]
                quick_buttons.append(("↩️ ย้อนกลับ", "แนะนำ"))
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(
                        text="🛠️ บริการของเรา:\nเลือกประเภทบริการที่คุณสนใจ 🔽",
                        quick_reply=build_quick_reply_with_extra(quick_buttons)
                    )
                )
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="ขออภัยค่ะ ขณะนี้ยังไม่พบบริการในระบบ")
                )

        # 12.1️⃣ ผู้ใช้เลือกหมวดหมู่บริการ
        elif (category := get_services_by_category(text)):
            flex_content = build_service_list_flex(text, category)
            flex_msg = FlexSendMessage(
                alt_text=f"บริการหมวด {text}",
                contents=flex_content
            )
            quick_buttons = [
                ("↩️ ย้อนกลับ", "บริการ"),
                ("🏠 เมนูหลัก", "แนะนำ")
            ]
            quick_reply_msg = TextSendMessage(
                text="เลือกบริการเพิ่มเติมหรือกลับไปเมนูหลัก",
                quick_reply=build_quick_reply_with_extra(quick_buttons)
            )
            line_bot_api.reply_message(reply_token, [flex_msg, quick_reply_msg])

        # 13️⃣ ไม่เข้าเงื่อนไข → ส่งไป Make
        else:
            print("❗️ไม่เข้าเงื่อนไข → ส่งไปถาม Make")
            answer = forward_to_make({
                "replyToken": reply_token,
                "userId": user_id,
                "text": text
            }) 

            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text=answer)
            )

    except Exception as e:
        print("Error in handle_message:", e)


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    reply_token = event.reply_token
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(
            text="ขอบคุณสำหรับสติ๊กเกอร์นะคะ 😊\nต้องการให้เราช่วยอะไรดีคะ👇",
            quick_reply=build_quick_reply_with_extra([
                ("🚗 เริ่มต้นเลือกยาง", "แนะนำ"),
                ("🛠️ บริการ", "บริการ"),
                ("🎉 โปรโมชัน", "โปรโมชัน"),
                ("📍 ร้านอยู่ที่ไหน", "ร้านอยู่ไหน"),
                ("📞 ติดต่อร้าน", "ติดต่อร้าน")
            ])
        )
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
