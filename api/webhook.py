import os
import sys
import re
from urllib.parse import quote
from werkzeug.utils import secure_filename

import mysql.connector
from flask import (
    Flask,
    request,
    abort,
    jsonify,
    send_from_directory,
    url_for,
)

import config
from make_integration import forward_to_make
from chatpdf_integration import forward_to_chatpdf
from db_queries import (
    get_active_promotions,
    get_all_tire_brands,
    get_tire_models_by_brand_id,
    get_tire_model_by_name,
    get_tires_by_model_id,
    get_tires_by_model_name,
    get_all_service_categories,
    get_services_by_category,
    get_models_by_brand,
    get_tire_model_image,
)
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction,
    FlexSendMessage,
    LocationSendMessage,
    StickerMessage,
    PostbackEvent,
)


LINE_CHANNEL_ACCESS_TOKEN = config.LINE_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET = config.LINE_CHANNEL_SECRET

app = Flask(__name__, static_folder="static")
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")


user_pages = {}

# Helper to manage per-user interaction mode
def set_user_mode(user_id, mode):
    if user_id not in user_pages:
        user_pages[user_id] = {}
    user_pages[user_id]["mode"] = mode


@app.route("/api/webhook", methods=["POST"])
def callback():
    body = request.get_data(as_text=True)
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


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "static", "images2")


# เส้นทางสำหรับรูปใน uploads/tires
@app.route("/static/uploads/tires/<path:filename>")
def tires_static(filename):
    tire_dir = os.path.join(BASE_DIR, "static", "uploads", "tires")
    print("Serving tire image:", os.path.join(tire_dir, filename))
    return send_from_directory(tire_dir, filename)


@app.route("/", methods=["GET", "POST"])
def home():
    return "LINE Bot Webhook is running!", 200


def file_exists(filename):
    if not filename:
        return False
    norm = str(filename).replace("\\", "/").lstrip("/")
    # If includes subpath, check under static root; otherwise default to images2
    if "/" in norm:
        return os.path.isfile(os.path.join("static", norm))
    return os.path.isfile(os.path.join("static", "images2", norm))


def get_image_url(filename):
    # ใช้ BASE_URL ที่กำหนดไว้ในไฟล์
    base_url = BASE_URL.rstrip("/")
    
    # ลบ /app ออกถ้ามี (สำหรับ Railway deployment)
    if base_url.endswith("/app"):
        base_url = base_url[:-4]

    # ถ้าเป็น URL จริง ให้ใช้เลย
    if filename and (str(filename).startswith("http://") or str(filename).startswith("https://")):
        return str(filename)

    # Normalize
    norm = (str(filename) if filename else "").replace("\\", "/").lstrip("/")
    if not norm:
        norm = "default-tire.jpg"

    # สร้าง URL โดยไม่ตรวจสอบไฟล์ (เพราะใน production ไม่สามารถเข้าถึงไฟล์ได้)
    from urllib.parse import quote
    if base_url:
        url = f"{base_url}/static/uploads/tires/{quote(norm)}"
    else:
        url = f"/static/uploads/tires/{quote(norm)}"

    # cache-busting ด้วย timestamp
    import time
    try:
        mtime = int(time.time())
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}v={mtime}"
    except Exception:
        pass

    print("IMAGE URL ที่สร้าง:", url)
    return url


def build_quick_reply(buttons):
    """สร้าง Quick Reply ตามปุ่มที่ส่งมา"""
    return QuickReply(
        items=[QuickReplyButton(action=MessageAction(label=label, text=text)) for label, text in buttons]
    )


def build_quick_reply_with_extra(buttons):
    """เหมือน build_quick_reply แต่บังคับเพิ่มปุ่ม ❓ ถามคำถามอื่น ไว้หน้าสุด"""
    extra_button = ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
    # หา index ของปุ่มเมนูหลัก (โดยดูจาก text == "แนะนำ" หรือ label มีคำว่า เมนูหลัก)
    main_menu_idx = None
    for idx, (label, text) in enumerate(buttons):
        if text == "แนะนำ" or ("เมนูหลัก" in str(label)):
            main_menu_idx = idx
            break

    # ถ้ามีปุ่ม "ถามเพิ่มเติม" อยู่แล้ว ให้ย้ายให้อยู่ก่อนหน้าเมนูหลัก
    if extra_button in buttons:
        if main_menu_idx is not None:
            # ลบตำแหน่งเดิมก่อน แล้วแทรกใหม่ก่อนหน้าเมนูหลัก
            buttons.remove(extra_button)
            buttons.insert(main_menu_idx, extra_button)
        else:
            # ไม่มีเมนูหลัก -> ให้ปุ่มนี้อยู่หน้าสุด
            buttons.remove(extra_button)
        buttons.insert(0, extra_button)
    else:
        # ยังไม่มีปุ่ม -> เพิ่มเข้าไปก่อนหน้าเมนูหลัก ถ้ามี; ไม่งั้นเพิ่มไว้หน้าสุด
        if main_menu_idx is not None:
            buttons.insert(main_menu_idx, extra_button)
        else:
            buttons.insert(0, extra_button)

    return build_quick_reply(buttons)


def build_selection_list_flex(title_text, option_labels):
    """สร้าง Flex Bubble ที่มีหัวข้อและปุ่มรายการแบบการ์ด (คล้ายภาพตัวอย่าง)
    - title_text: ข้อความหัวข้อ
    - option_labels: list ของข้อความปุ่ม (กดแล้วส่งข้อความเดียวกันกลับมา)
    """
    buttons = []
    for label in option_labels:
        buttons.append({
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#E9ECF1",
            "cornerRadius": "md",
            "paddingAll": "12px",
            "margin": "md",
            "action": {
                "type": "message",
                "label": label,
                "text": label,
            },
            "contents": [
                {
                    "type": "text",
                    "text": label,
                    "align": "center",
                    "color": "#1F2937",
                    "weight": "bold",
                }
            ],
        })

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title_text,
                    "weight": "bold",
                    "size": "md",
                    "wrap": True,
                },
                {"type": "separator", "margin": "md"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "sm",
                    "contents": buttons,
                },
            ],
        },
    }
    return bubble


def build_tire_flex(tire):
    """สร้าง Flex Message สำหรับแสดงข้อมูลยาง"""
    image_url = get_image_url(tire.get("tire_image_url"))
    
    # สร้าง URL สำหรับลิงก์ไปยังหน้าเว็บไซต์ตามรุ่นยางในฐานข้อมูล
    base_url = "https://webtire-production.up.railway.app"
    
    # ดึงข้อมูลยี่ห้อและรุ่นจาก tire object
    brand_name = tire.get('brand_name', '')
    model_name_clean = tire.get('model_name', '')
    
    print(f"Debug - build_tire_flex: brand_name='{brand_name}', model_name='{model_name_clean}'")
    
    # สร้าง URL แบบเฉพาะเจาะจงตามรูปแบบ /tires/{brand}?model={model}
    if brand_name and model_name_clean:
        # URL encode สำหรับชื่อยี่ห้อและรุ่น
        from urllib.parse import quote
        # แปลงชื่อยี่ห้อเป็นตัวเล็กเพื่อให้ตรงกับ URL
        brand_lower = brand_name.lower()
        brand_encoded = quote(brand_lower)
        model_encoded = quote(model_name_clean)
        
        # ใช้ URL format ที่เว็บไซต์รองรับ (เหมือนกับใน build_michelin_model_flex)
        tire_url = f"{base_url}/tires/{brand_encoded}?model={model_encoded}"
        print(f"Debug - Generated specific URL: {tire_url}")
    else:
        # ถ้าไม่มีข้อมูลยี่ห้อหรือรุ่น ให้ไปยังหน้าเว็บไซต์หลัก
        tire_url = f"{base_url}/tires"
        print(f"Debug - Using default URL: {tire_url}")
    
    return {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectRatio": "4:3",
            "aspectMode": "fit",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": model_name_clean or tire.get('model_name', '') or "Unknown Model",
                    "weight": "bold",
                    "size": "xl",
                    "wrap": True,
                    "color": "#0B4F6C",
                },
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
                        {"type": "text", "text": f"🔥 โปรพิเศษ: {tire.get('promotion_price') or '-'} บาท"},
                    ],
                },
            ],
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "🔗 ดูรายละเอียดเพิ่มเติม",
                        "uri": tire_url
                    }
                }
            ]
        }
    }


def build_michelin_model_flex():
    """สร้าง Flex Message แสดงรุ่นยาง Michelin พร้อมลิงก์"""
    # ดึงข้อมูลรุ่นยาง Michelin จากฐานข้อมูล
    michelin_models = get_models_by_brand("Michelin")
    
    bubbles = []
    for model in michelin_models:
        model_name = model.get("model_name", "")
        tire_category = model.get("tire_category", "ไม่ระบุ")
        
        # กำหนดรูปภาพตามรุ่นยาง
        image_url = get_tire_model_image(model_name)
        
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": image_url,
                "size": "full",
                "aspectRatio": "4:3",
                "aspectMode": "fit",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"Michelin {model_name}",
                        "weight": "bold",
                        "size": "lg",
                        "wrap": True,
                        "color": "#0B4F6C"
                    },
                    {
                        "type": "text",
                        "text": f"หมวด: {tire_category}",
                        "size": "sm",
                        "color": "#666666",
                        "margin": "sm"
                    }
                ],
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "ดูรายละเอียดและราคา",
                            "data": f"model={model_name}"
                        }
                    }
                ]
            }
        }
        bubbles.append(bubble)
    
    return {"type": "carousel", "contents": bubbles}


def build_bfgoodrich_model_flex():
    """สร้าง Flex Message แสดงรุ่นยาง BFGoodrich พร้อมลิงก์"""
    # ดึงข้อมูลรุ่นยาง BFGoodrich จากฐานข้อมูล
    bfgoodrich_models = get_models_by_brand("BFGoodrich")
    
    bubbles = []
    for model in bfgoodrich_models:
        model_name = model.get("model_name", "")
        tire_category = model.get("tire_category", "ไม่ระบุ")
        
        # กำหนดรูปภาพตามรุ่นยาง
        image_url = get_tire_model_image(model_name)
        
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": image_url,
                "size": "full",
                "aspectRatio": "4:3",
                "aspectMode": "fit",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"BFGoodrich {model_name}",
                        "weight": "bold",
                        "size": "lg",
                        "wrap": True,
                        "color": "#0B4F6C"
                    },
                    {
                        "type": "text",
                        "text": f"หมวด: {tire_category}",
                        "size": "sm",
                        "color": "#666666",
                        "margin": "sm"
                    }
                ],
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "ดูรายละเอียดและราคา",
                            "data": f"model={model_name}"
                        }
                    }
                ]
            }
        }
        bubbles.append(bubble)
    
    return {"type": "carousel", "contents": bubbles}


def build_maxxis_model_flex():
    """สร้าง Flex Message แสดงรุ่นยาง Maxxis พร้อมลิงก์"""
    # ดึงข้อมูลรุ่นยาง Maxxis จากฐานข้อมูล
    maxxis_models = get_models_by_brand("Maxxis")
    
    bubbles = []
    for model in maxxis_models:
        model_name = model.get("model_name", "")
        tire_category = model.get("tire_category", "ไม่ระบุ")
        
        # กำหนดรูปภาพตามรุ่นยาง
        image_url = get_tire_model_image(model_name)
        
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": image_url,
                "size": "full",
                "aspectRatio": "4:3",
                "aspectMode": "fit",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"Maxxis {model_name}",
                        "weight": "bold",
                        "size": "lg",
                        "wrap": True,
                        "color": "#0B4F6C"
                    },
                    {
                        "type": "text",
                        "text": f"หมวด: {tire_category}",
                        "size": "sm",
                        "color": "#666666",
                        "margin": "sm"
                    }
                ],
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "ดูรายละเอียดและราคา",
                            "data": f"model={model_name}"
                        }
                    }
                ]
            }
        }
        bubbles.append(bubble)
    
    return {"type": "carousel", "contents": bubbles}


def build_promotion_flex(promo, index=0):
    image_url = get_image_url(promo.get("image_url"))
    if not image_url or "http" not in image_url:
        image_url = "https://placeholder.vercel.app/images/default-promotion.jpg"
    
    # ตัดข้อความ description ให้สั้นลง (ไม่เกิน 100 ตัวอักษร)
    description = promo.get("description", "-")
    if len(description) > 100:
        description = description[:97] + "..."
    
    # กำหนดลิงก์ตาม index
    promotion_links = {
        0: "https://webtire-production.up.railway.app/promotions/13",
        1: "https://webtire-production.up.railway.app/promotions/14",
        2: "https://webtire-production.up.railway.app/promotions/15",
        3: "https://webtire-production.up.railway.app/promotions/16",
        4: "https://webtire-production.up.railway.app/promotions/17",
        5: "https://webtire-production.up.railway.app/promotions/18"
    }
    
    bubble = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectRatio": "4:3",
            "aspectMode": "fit",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": promo.get("title", "-"), "weight": "bold", "size": "lg", "wrap": True},
                {"type": "text", "text": description, "size": "sm", "wrap": True, "margin": "md"},
                {"type": "text", "text": f"📅 {promo['start_date']} ถึง {promo['end_date']}", "size": "xs", "color": "#888888", "margin": "md"},
            ],
        },
    }
    
    # เพิ่มลิงก์สำหรับโปรโมชันที่มีลิงก์กำหนด
    if index in promotion_links:
        bubble["footer"] = {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "ดูรายละเอียดเพิ่มเติม",
                        "uri": promotion_links[index]
                    }
                }
            ]
        }
    
    return bubble


def build_service_list_flex(category_name, services):
    """สร้าง Flex Message แสดงรายการบริการแบบง่ายๆ"""
    service_items = []
    for service in services:
        service_contents = [
            {
                "type": "text",
                "text": service.get("service_name", "ไม่ระบุ"),
                "size": "sm",
                "weight": "bold",
                "wrap": True,
            }
        ]

        service_item = {
            "type": "box",
            "layout": "horizontal",
            "margin": "sm",
            "spacing": "sm",
            "contents": [
                {"type": "text", "text": "🔧", "size": "sm", "flex": 0},
                {"type": "box", "layout": "vertical", "flex": 1, "contents": service_contents},
            ],
        }
        service_items.append(service_item)

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
                    "color": "#FFFFFF",
                }
            ],
            "backgroundColor": "#1EC445C5",
            "paddingAll": "md",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": service_items,
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "action": {
                        "type": "message",
                        "label": "↩️ กลับไปเลือกหมวดบริการ",
                        "text": "บริการ",
                    },
                }
            ],
        },
    }


def get_tire_model_name_by_id(model_id):
    """ดึงชื่อรุ่นยางตาม model_id"""
    from db_queries import get_tire_model_name_by_id as db_get_tire_model_name_by_id
    result = db_get_tire_model_name_by_id(model_id)
    if result:
        return result
    else:
        return {"model_id": model_id, "model_name": "Unknown Model", "brand_name": "Unknown Brand", "tire_category": "ไม่ระบุ"}


def create_sample_tires_for_model(model_name, brand_name, tire_category):
    """สร้างข้อมูลยางตัวอย่างสำหรับรุ่นที่ไม่มีข้อมูลในฐานข้อมูล"""
    print(f"Debug - Creating sample tires for {brand_name} {model_name}")
    
    # กำหนดข้อมูลยางตัวอย่างตามรุ่น
    sample_tires = []
    
    if brand_name.lower() == "michelin":
        if model_name.upper() == "EXM2+":
            # ใช้ข้อมูลยางจากฐานข้อมูลที่ใช้ model_id = 1
            sample_tires = [
                {
                    "tire_id": 42,
                    "full_size": "175/70 R13 82T TL",
                    "load_index": "82",
                    "speed_symbol": "T",
                    "ply_rating": None,
                    "price_each": 2750.00,
                    "price_set": 11000.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_ENERGY_XM2_+_EXM2+.png"
                },
                {
                    "tire_id": 43,
                    "full_size": "185/70 R13 86T TL",
                    "load_index": "86",
                    "speed_symbol": "T",
                    "ply_rating": None,
                    "price_each": 2850.00,
                    "price_set": 11400.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_ENERGY_XM2_+_EXM2+.png"
                },
                {
                    "tire_id": 44,
                    "full_size": "165/65 R14 79H TL",
                    "load_index": "79",
                    "speed_symbol": "H",
                    "ply_rating": None,
                    "price_each": 2850.00,
                    "price_set": 11400.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_ENERGY_XM2_+_EXM2+.png"
                },
                {
                    "tire_id": 45,
                    "full_size": "165/70 R14 81T TL",
                    "load_index": "81",
                    "speed_symbol": "T",
                    "ply_rating": None,
                    "price_each": 2950.00,
                    "price_set": 11800.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_ENERGY_XM2_+_EXM2+.png"
                },
                {
                    "tire_id": 46,
                    "full_size": "175/65 R14 82H TL",
                    "load_index": "82",
                    "speed_symbol": "H",
                    "ply_rating": None,
                    "price_each": 2950.00,
                    "price_set": 11800.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_ENERGY_XM2_+_EXM2+.png"
                },
                {
                    "tire_id": 47,
                    "full_size": "175/70 R14 88T XL TL",
                    "load_index": "88",
                    "speed_symbol": "T",
                    "ply_rating": None,
                    "price_each": 3250.00,
                    "price_set": 13000.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_ENERGY_XM2_+_EXM2+.png"
                },
                {
                    "tire_id": 48,
                    "full_size": "185/60 R14 82H TL",
                    "load_index": "82",
                    "speed_symbol": "H",
                    "ply_rating": None,
                    "price_each": 3300.00,
                    "price_set": 13200.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_ENERGY_XM2_+_EXM2+.png"
                },
                {
                    "tire_id": 49,
                    "full_size": "185/65 R14 86H TL",
                    "load_index": "86",
                    "speed_symbol": "H",
                    "ply_rating": None,
                    "price_each": 3100.00,
                    "price_set": 12400.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_ENERGY_XM2_+_EXM2+.png"
                },
                {
                    "tire_id": 50,
                    "full_size": "185/70 R14 88H TL",
                    "load_index": "88",
                    "speed_symbol": "H",
                    "ply_rating": None,
                    "price_each": 3300.00,
                    "price_set": 13200.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_ENERGY_XM2_+_EXM2+.png"
                },
                {
                    "tire_id": 51,
                    "full_size": "195/60 R14 86H TL",
                    "load_index": "86",
                    "speed_symbol": "H",
                    "ply_rating": None,
                    "price_each": 3600.00,
                    "price_set": 14400.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_ENERGY_XM2_+_EXM2+.png"
                },
                {
                    "tire_id": 52,
                    "full_size": "195/70 R14 91H TL",
                    "load_index": "91",
                    "speed_symbol": "H",
                    "ply_rating": None,
                    "price_each": 3650.00,
                    "price_set": 14600.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_ENERGY_XM2_+_EXM2+.png"
                }
            ]
        elif model_name.upper() == "ENERGY XM2+":
            # ใช้ข้อมูลยางจากฐานข้อมูลที่ใช้ model_id = 2
            sample_tires = [
                {
                    "tire_id": 53,
                    "full_size": "175/65 R15 84H TL",
                    "load_index": "84",
                    "speed_symbol": "H",
                    "ply_rating": None,
                    "price_each": 2650.00,
                    "price_set": 10600.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_ENERGY_XM2_+_EXM2+.png"
                },
                {
                    "tire_id": 54,
                    "full_size": "185/60 R15 84H TL",
                    "load_index": "84",
                    "speed_symbol": "H",
                    "ply_rating": None,
                    "price_each": 2650.00,
                    "price_set": 10600.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_ENERGY_XM2_+_EXM2+.png"
                }
            ]
        elif model_name.upper() == "AGILIS3":
            sample_tires = [
                {
                    "tire_id": 9998,
                    "full_size": "195/80 R14 106/104R",
                    "load_index": "106/104",
                    "speed_symbol": "R",
                    "ply_rating": None,
                    "price_each": 2700.00,
                    "price_set": 10800.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_AGILIS_3.png"
                },
                {
                    "tire_id": 9999,
                    "full_size": "205/75 R14C 109/107R TL",
                    "load_index": "109/107",
                    "speed_symbol": "R",
                    "ply_rating": None,
                    "price_each": 3300.00,
                    "price_set": 13200.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_AGILIS_3.png"
                }
            ]
        elif model_name.upper() == "XCD2":
            sample_tires = [
                {
                    "tire_id": 10000,
                    "full_size": "205/75 R14C 109/107P TL PR8",
                    "load_index": "109/107",
                    "speed_symbol": "P",
                    "ply_rating": "PR8",
                    "price_each": 3450.00,
                    "price_set": 13800.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_XCD_2.png"
                },
                {
                    "tire_id": 10001,
                    "full_size": "215/75 R14C 112/110P TL PR8",
                    "load_index": "112/110",
                    "speed_symbol": "P",
                    "ply_rating": "PR8",
                    "price_each": 3850.00,
                    "price_set": 15400.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_XCD_2.png"
                }
            ]
        elif model_name.upper() == "PRIMACRY SUV+":
            sample_tires = [
                {
                    "tire_id": 10002,
                    "full_size": "205/70 R15 96H TL",
                    "load_index": "96",
                    "speed_symbol": "H",
                    "ply_rating": None,
                    "price_each": 4650.00,
                    "price_set": 18600.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_PRIMACRY_SUV+.png"
                },
                {
                    "tire_id": 10003,
                    "full_size": "215/70 R16 100H TL",
                    "load_index": "100",
                    "speed_symbol": "H",
                    "ply_rating": None,
                    "price_each": 5750.00,
                    "price_set": 23000.00,
                    "promotion_price": None,
                    "tire_image_url": "Michelin_PRIMACRY_SUV+.png"
                }
            ]
    
    print(f"Debug - Created {len(sample_tires)} sample tires")
    return sample_tires



def build_promotion_flex(promo, index=0):
    image_url = get_image_url(promo.get("image_url"))
    if not image_url or "http" not in image_url:
        image_url = "https://placeholder.vercel.app/images/default-promotion.jpg"

    # ตัดข้อความ description ให้สั้นลง (ไม่เกิน 100 ตัวอักษร)
    description = promo.get("description", "-")
    if len(description) > 100:
        description = description[:97] + "..."

    # กำหนดลิงก์ตาม index
    promotion_links = {
        0: "https://webtire-production.up.railway.app/promotions/13",
        1: "https://webtire-production.up.railway.app/promotions/14", 
        2: "https://webtire-production.up.railway.app/promotions/15",
        3: "https://webtire-production.up.railway.app/promotions/16",
        4: "https://webtire-production.up.railway.app/promotions/17",
        5: "https://webtire-production.up.railway.app/promotions/18"
    }

    bubble = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectRatio": "4:3",
            "aspectMode": "fit",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": promo.get("title", "-"), "weight": "bold", "size": "lg", "wrap": True},
                {"type": "text", "text": description, "size": "sm", "wrap": True, "margin": "md"},
                {"type": "text", "text": f"📅 {promo['start_date']} ถึง {promo['end_date']}", "size": "xs", "color": "#888888", "margin": "md"},
            ],
        },
    }
    
    # เพิ่มลิงก์สำหรับโปรโมชันที่มีลิงก์กำหนด
    if index in promotion_links:
        bubble["footer"] = {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "ดูรายละเอียดเพิ่มเติม",
                        "uri": promotion_links[index]
                    }
                }
            ]
        }
    
    return bubble


def send_tires_page(reply_token, user_id):
    if user_id not in user_pages:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="กรุณาเลือกยี่ห้อและรุ่นก่อน"))
        return

    page_size = 8  # ลดลงเพื่อให้ไม่เกิน 12 รายการที่ LINE Bot จำกัด
    page = user_pages[user_id]["page"]
    model_id = user_pages[user_id]["model_id"]

    tires = get_tires_by_model_id(model_id)
    if not tires:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="ไม่พบข้อมูลยาง"))
        return

    start = (page - 1) * page_size
    end = start + page_size
    tires_page = tires[start:end]

    tire_model = get_tire_model_name_by_id(model_id)
    model_name = tire_model.get("model_name", "Unknown Model")
    
    print(f"Debug - send_tires_page: tire_model={tire_model}")
    print(f"Debug - send_tires_page: model_name={model_name}")

    bubbles = []
    for t in tires_page:
        # เพิ่มข้อมูลยี่ห้อและรุ่นใน tire object
        t['brand_name'] = tire_model.get("brand_name", "")
        t['model_name'] = tire_model.get("model_name", "")
        print(f"Debug - send_tires_page: tire object after adding model_name: {t}")
        tire_flex = build_tire_flex(t)
        bubbles.append(tire_flex)
    carousel = {"type": "carousel", "contents": bubbles}
    flex_msg = FlexSendMessage(alt_text=f"ข้อมูลยางรุ่นหน้า {page}", contents=carousel)

    nav_buttons = []
    if page > 1:
        nav_buttons.append(("⬅️ ก่อนหน้า", f"page_{page - 1}"))
    if end < len(tires):
        nav_buttons.append(("ยางรุ่นที่เลือกหน้าถัดไป ➡️", f"page_{page + 1}"))

    nav_buttons.extend([
        ("↩️ เลือกรุ่นอื่น", "ยี่ห้อยางรถยนต์"),
        ("🏠 เมนูหลัก", "แนะนำ"),
    ])

    line_bot_api.reply_message(
        reply_token,
        [
            flex_msg,
            TextSendMessage(
                text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                quick_reply=build_quick_reply_with_extra(nav_buttons),
            ),
        ],
    )


def find_brand_in_text(text):
    text_lower = text.lower()
    brands = get_all_tire_brands()
    for b in brands:
        if b["brand_name"].lower() in text_lower:
            return b
    return None


def find_model_in_text(text):
    text_lower = text.lower()
    all_brands = get_all_tire_brands()
    print(f"Debug - Searching for model: '{text}'")
    
    for b in all_brands:
        models = get_tire_models_by_brand_id(b["brand_id"])
        for m in models:
            model_name_lower = m["model_name"].lower()
            print(f"Debug - Checking model: '{m['model_name']}' against '{text}'")
            
            # ลองหลายวิธีในการจับคู่
            if (model_name_lower in text_lower or 
                text_lower in model_name_lower or
                text_lower.replace('+', '').replace(' ', '') in model_name_lower.replace('+', '').replace(' ', '') or
                model_name_lower.replace('+', '').replace(' ', '') in text_lower.replace('+', '').replace(' ', '')):
                print(f"Debug - Found match: '{m['model_name']}'")
                # เพิ่มข้อมูลยี่ห้อ
                m['brand_name'] = b['brand_name']
                return m
    print(f"Debug - No model match found for: '{text}'")
    return None


def find_model_by_alias(text):
    """ค้นหารุ่นยางโดยใช้ชื่อย่อหรือชื่อที่ใช้กันทั่วไป"""
    text_upper = text.upper()
    print(f"Debug - Alias search for: '{text_upper}'")
    
    # ค้นหาโดยตรงในฐานข้อมูลก่อน
    all_brands = get_all_tire_brands()
    for b in all_brands:
        models = get_tire_models_by_brand_id(b["brand_id"])
        for m in models:
            model_name_upper = m["model_name"].upper()
            print(f"Debug - Checking alias: '{text_upper}' against '{model_name_upper}'")
            
            # ตรวจสอบการจับคู่แบบต่างๆ
            if (text_upper == model_name_upper or
                text_upper in model_name_upper or
                model_name_upper in text_upper or
                text_upper.replace('+', '') == model_name_upper.replace('+', '') or
                text_upper.replace('+', '') in model_name_upper.replace('+', '') or
                model_name_upper.replace('+', '') in text_upper.replace('+', '')):
                print(f"Debug - Found alias match: '{m['model_name']}'")
                # เพิ่มข้อมูลยี่ห้อ
                m['brand_name'] = b['brand_name']
                return m
    
    return None


def debug_all_models():
    """แสดงรุ่นยางทั้งหมดในฐานข้อมูลเพื่อ debug"""
    print("=== DEBUG: All models in database ===")
    all_brands = get_all_tire_brands()
    for b in all_brands:
        print(f"Brand: {b['brand_name']}")
        models = get_tire_models_by_brand_id(b["brand_id"])
        for m in models:
            print(f"  - Model: '{m['model_name']}'")
    print("=== End debug ===")


def find_promotion_in_text(text):
    text_lower = text.lower()
    promotions = get_active_promotions()
    for p in promotions:
        if p["title"].lower() in text_lower:
            return p
    return None


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()
    reply_token = event.reply_token
    user_id = event.source.user_id
    mode = user_pages.get(user_id, {}).get("mode", "menu")

    # Debug: แสดงข้อความที่ได้รับ
    print(f"Received text: '{text}' from user: {user_id}")
    print(f"Text type: {type(text)}, Length: {len(text)}")
    
    # ตรวจสอบ reply_token
    if not reply_token:
        print("❌ No reply token available")
        return
    
    # Debug: แสดงรุ่นยางทั้งหมดในฐานข้อมูล (เฉพาะครั้งแรก)
    if not hasattr(debug_all_models, '_called'):
        debug_all_models()
        debug_all_models._called = True

    try:
        # จัดการ pagination ก่อน
        if text.startswith("page_"):
            set_user_mode(user_id, "menu")
            try:
                page_num = int(text.split("_")[1])
                print(f"Debug - Page navigation: user_id={user_id}, page={page_num}")
                print(f"Debug - user_pages: {user_pages}")
                
                if user_id in user_pages and "model_id" in user_pages[user_id]:
                    user_pages[user_id]["page"] = page_num
                    print(f"Debug - Updated page to {page_num} for user {user_id}")
                    send_tires_page(reply_token, user_id)
                else:
                    print(f"Debug - User {user_id} not found in user_pages or missing model_id")
                    line_bot_api.reply_message(
                        reply_token,
                        TextSendMessage(text="กรุณาเลือกยี่ห้อและรุ่นก่อนค่ะ"),
                    )
            except Exception as e:
                print(f"Debug - Error in page navigation: {e}")
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text=f"เกิดข้อผิดพลาด: {str(e)}"),
                )
            return
        
        # จัดการ Quick Reply เกี่ยวกับยาง (ไม่เรียก Make)
        if text in ["แนะนำ", "ยี่ห้อยางรถยนต์", "รุ่น", "บริการ", "โปรโมชัน", "ร้านอยู่ไหน", "ติดต่อร้าน"]:
            # เปลี่ยน mode เป็น menu เมื่อกด Quick Reply
            set_user_mode(user_id, "menu")
            # ไม่ต้องไปเรียก Make integration แต่ให้ระบบทำงานต่อ
            pass
        
        # จัดการคำเฉพาะที่ต้องแสดงข้อมูลทันที
        if text == "โปรโมชัน":
            set_user_mode(user_id, "menu")
            promotions = get_active_promotions()
            if not promotions:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="ขณะนี้ยังไม่มีโปรโมชันค่ะ"),
                )
            else:
                bubbles = [build_promotion_flex(p, i) for i, p in enumerate(promotions[:10])]
                carousel = {"type": "carousel", "contents": bubbles}
                line_bot_api.reply_message(
                    reply_token,
                    [
                        FlexSendMessage(alt_text="โปรโมชัน", contents=carousel),
                        TextSendMessage(
                            text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                            quick_reply=build_quick_reply([
                                ("🏠 เมนูหลัก", "แนะนำ"),
                                ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                            ])
                        )
                    ]
                )
            return
            
        elif text == "บริการ":
            set_user_mode(user_id, "menu")
            service_categories = get_all_service_categories()
            if service_categories:
                bubble = build_selection_list_flex("🛠️ เลือกบริการ", [cat["category"] for cat in service_categories[:12]])
                line_bot_api.reply_message(
                    reply_token, 
                    [
                        FlexSendMessage(alt_text="เลือกบริการ", contents=bubble),
                        TextSendMessage(
                            text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                            quick_reply=build_quick_reply([
                                ("🏠 เมนูหลัก", "แนะนำ"),
                                ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                            ])
                        )
                    ]
                )
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="ขออภัยค่ะ ขณะนี้ยังไม่พบบริการในระบบ"),
                )
            return
        
        # จัดการคำถามเพิ่มเติม (เรียก Make)
        elif text == "ถามเพิ่มเติม":
            # เปลี่ยน mode เป็น free_text เพื่อให้เรียก Make
            set_user_mode(user_id, "free_text")
            
            # แสดงตัวอย่างคำถามที่สามารถถามได้
            example_questions = [
                "ยางแบบไหนเหมาะกับรถกระบะ?",
                "ยางแบบไหนเหมาะกับรถเก๋ง?",
                "ยางแบบไหนเหมาะกับขับเร็ว?"
            ]
            
            # สร้าง Flex Message แสดงตัวอย่างคำถาม
            bubbles = []
            for i, question in enumerate(example_questions[:8]):  # แสดง 8 คำถาม
                bubble = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"💡 {question}",
                                "wrap": True,
                                "size": "sm",
                                "color": "#666666"
                            }
                        ],
                        "paddingAll": "12px"
                    },
                    "action": {
                        "type": "postback",
                        "label": "ถามคำถามนี้",
                        "data": f"ask_question={question}"
                    }
                }
                bubbles.append(bubble)
            
            carousel = {"type": "carousel", "contents": bubbles}
            
            line_bot_api.reply_message(
                reply_token,
                [
                    TextSendMessage(text="💬 คุณสามารถถามคำถามเกี่ยวกับยางได้เลยค่ะ! ตัวอย่างคำถามที่ถามได้บ่อย:"),
                    FlexSendMessage(alt_text="ตัวอย่างคำถาม", contents=carousel),
                    TextSendMessage(
                        text="📝 หรือพิมพ์คำถามของคุณเองได้เลยค่ะ\n\n💡 หากต้องการออกจากโหมดถามเพิ่มเติม ให้พิมพ์ 'แนะนำ' ค่ะ",
                        quick_reply=build_quick_reply([
                            ("🏠 เมนูหลัก", "แนะนำ"),
                            ("🔙 กลับ", "แนะนำ")
                        ])
                    )
                ]
            )
            return
        
        # In free_text mode, forward to Make unless user types a known navigation command
        if mode == "free_text":
            navigation_triggers = [
                "แนะนำ",
                "ยี่ห้อ",
                "รุ่น",
                "ร้านอยู่ไหน",
                "ติดต่อ",
                "ติดต่อร้าน",
                "ติดต่อร้านยาง",
                "ติดต่อเรา",
                "เบอร์โทร",
                "โทรศัพท์",
                "เวลาเปิดทำการ",
                "บริการ",
                "โปร",
                "promotion",
                "โปรโมชัน",
                "service",
                "เมนูหลัก",
            ]
            if not any(trigger in text for trigger in navigation_triggers):
                try:
                    make_answer = forward_to_make({
                        "replyToken": reply_token,
                        "userId": user_id,
                        "text": text,
                    })
                    if make_answer:
                        line_bot_api.reply_message(reply_token, TextSendMessage(text=make_answer))
                except Exception as make_err:
                    print("❌ Make error:", make_err)
                return

        if any(word in text.lower() for word in ["สวัสดี", "hello", "hi", "หวัดดี"]):
            set_user_mode(user_id, "menu")
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(
                    text="สวัสดีค่ะ 😊 ยินดีต้อนรับสู่ร้านยางของเราค่ะ\nต้องการให้ช่วยเรื่องอะไรดีคะ ",
                    quick_reply=build_quick_reply_with_extra([
                        ("🚗 แนะนำยาง", "แนะนำ"),
                        ("🛠️ บริการ", "บริการ"),
                        ("🎉 โปรโมชัน", "โปรโมชัน"),
                        ("📍 ร้านอยู่ที่ไหน", "ร้านอยู่ไหน"),
                        ("📞 ติดต่อร้าน", "ติดต่อร้าน"),
                    ]),
                ),
            )

        # --- 3) ถามรุ่นยางทั้งหมด ---
        elif re.search(r"(มียางรุ่น(ไหน|อะไร)บ้าง|รุ่นอะไรบ้าง|เลือกรุ่น)", text):
            set_user_mode(user_id, "menu")
            brands = get_all_tire_brands()
            all_models = []
            for b in brands:
                models = get_tire_models_by_brand_id(b["brand_id"])
                if models:
                    all_models.extend([m for m in models])

            if all_models:
                # สร้าง Flex Message สำหรับแต่ละรุ่นยาง
                bubbles = []
                for model in all_models[:6]:  # จำกัดไว้ 6 รุ่น เพื่อให้ไม่เกิน 12 bubbles
                    brand_name = model.get('brand_name', '')
                    model_name = model.get('model_name', '')
                    
                    # ดึงข้อมูลยางของรุ่นนี้
                    model_id = model.get("model_id")
                    tires = get_tires_by_model_id(model_id)
                    
                    if tires:
                        # สร้าง Flex Message สำหรับแต่ละยาง
                        for tire in tires[:2]:  # จำกัดไว้ 2 รุ่นต่อรุ่นยาง
                            # เพิ่มข้อมูลยี่ห้อใน tire object
                            tire['brand_name'] = brand_name
                            tire_flex = build_tire_flex(tire)
                            bubbles.append(tire_flex)
                            
                            # จำกัดจำนวน bubbles ไม่เกิน 12
                            if len(bubbles) >= 12:
                                break
                    
                    # จำกัดจำนวน bubbles ไม่เกิน 12
                    if len(bubbles) >= 12:
                        break
                    else:
                        # ถ้าไม่มีข้อมูลยาง ให้แสดงข้อมูลรุ่น
                        bubble = {
                            "type": "bubble",
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"{brand_name} {model_name}",
                                        "weight": "bold",
                                        "size": "lg",
                                        "wrap": True,
                                        "color": "#0B4F6C"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"หมวด: {model.get('tire_category', 'ไม่ระบุ')}",
                                        "size": "sm",
                                        "color": "#666666",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "text",
                                        "text": "ไม่พบข้อมูลยางในระบบ",
                                        "size": "sm",
                                        "color": "#FF6B6B",
                                        "margin": "sm"
                                    }
                                ]
                            }
                        }
                        bubbles.append(bubble)
                
                # สร้าง Carousel (จำกัดไม่เกิน 12 รายการ)
                if len(bubbles) > 12:
                    bubbles = bubbles[:12]
                carousel = {"type": "carousel", "contents": bubbles}
                
                line_bot_api.reply_message(
                    reply_token,
                    [
                        FlexSendMessage(
                            alt_text="เลือกรุ่นยาง",
                            contents=carousel
                        ),
                        TextSendMessage(
                            text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                            quick_reply=build_quick_reply([
                                ("⬅️ กลับไปเลือกยี่ห้อ", "ยี่ห้อยางรถยนต์"),
                                ("🏠 เมนูหลัก", "แนะนำ"),
                                ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                            ])
                        )
                    ]
                )
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="ไม่พบข้อมูลรุ่นยางในระบบ")
                )
        # --- 4) ถามหายางที่เหมาะกับรถ (ส่งไป Make) ---
        elif re.search(r"(ยางที่เหมาะ|ยางรุ่นไหนเหมาะ|แนะนำยาง.*รถ|ยาง.*รถรุ่น)", text.lower()):
            try:
                make_answer = forward_to_make({
                    "replyToken": reply_token,
                    "userId": user_id,
                    "text": text,
                })
                if make_answer:
                    line_bot_api.reply_message(
                        reply_token,
                        TextSendMessage(text=make_answer)
                    )
            except Exception as make_err:
                print("❌ Make error:", make_err)
            return

        elif any(kw in text.lower() for kw in ["แนะนำ", "แนะนำยาง", "แนะนำหน่อย"]):
            set_user_mode(user_id, "menu")
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(
                    text="เลือกเมนูที่ต้องการได้เลยค่ะ ",
                    quick_reply=build_quick_reply([
                        ("🚗 ยี่ห้อยางรถยนต์", "ยี่ห้อยางรถยนต์"),
                        ("🛠️ บริการ", "บริการ"),
                        ("🎉 โปรโมชัน", "โปรโมชัน"),
                        ("📞 ติดต่อร้าน", "ติดต่อร้าน"),
                        ("🕗 เวลาเปิดทำการ", "เวลาเปิดทำการ"),
                    ]),
                ),
            )

        elif "ยี่ห้อยาง" in text:
            set_user_mode(user_id, "menu")
            brands = get_all_tire_brands()
            if brands:
                labels = [b["brand_name"] for b in brands[:12]]
                bubble = build_selection_list_flex("📌 เลือกยี่ห้อยาง", labels)
                line_bot_api.reply_message(
                    reply_token, 
                    [
                        FlexSendMessage(alt_text="เลือกรุ่นยี่ห้อ", contents=bubble),
                        TextSendMessage(
                            text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                            quick_reply=build_quick_reply([
                                ("🏠 เมนูหลัก", "แนะนำ"),
                                ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                            ])
                        )
                    ]
                )
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="ไม่พบข้อมูลยี่ห้อยางในระบบ"),
                )

        elif "รุ่น" in text:
            set_user_mode(user_id, "menu")
            brands = get_all_tire_brands()
            all_models = []
            for b in brands:
                models = get_tire_models_by_brand_id(b["brand_id"])
                if models:
                    all_models.extend([m for m in models])

            if all_models:
                # สร้าง Flex Message สำหรับแต่ละรุ่นยาง
                bubbles = []
                for model in all_models[:6]:  # จำกัดไว้ 6 รุ่น เพื่อให้ไม่เกิน 12 bubbles
                    brand_name = model.get('brand_name', '')
                    model_name = model.get('model_name', '')
                    
                    # ดึงข้อมูลยางของรุ่นนี้
                    model_id = model.get("model_id")
                    tires = get_tires_by_model_id(model_id)
                    
                    if tires:
                        # สร้าง Flex Message สำหรับแต่ละยาง
                        for tire in tires[:2]:  # จำกัดไว้ 2 รุ่นต่อรุ่นยาง
                            # เพิ่มข้อมูลยี่ห้อใน tire object
                            tire['brand_name'] = brand_name
                            tire_flex = build_tire_flex(tire)
                            bubbles.append(tire_flex)
                            
                            # จำกัดจำนวน bubbles ไม่เกิน 12
                            if len(bubbles) >= 12:
                                break
                    
                    # จำกัดจำนวน bubbles ไม่เกิน 12
                    if len(bubbles) >= 12:
                        break
                    else:
                        # ถ้าไม่มีข้อมูลยาง ให้แสดงข้อมูลรุ่น
                        bubble = {
                            "type": "bubble",
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"{brand_name} {model_name}",
                                        "weight": "bold",
                                        "size": "lg",
                                        "wrap": True,
                                        "color": "#0B4F6C"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"หมวด: {model.get('tire_category', 'ไม่ระบุ')}",
                                        "size": "sm",
                                        "color": "#666666",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "text",
                                        "text": "ไม่พบข้อมูลยางในระบบ",
                                        "size": "sm",
                                        "color": "#FF6B6B",
                                        "margin": "sm"
                                    }
                                ]
                            }
                        }
                        bubbles.append(bubble)
                
                # สร้าง Carousel (จำกัดไม่เกิน 12 รายการ)
                if len(bubbles) > 12:
                    bubbles = bubbles[:12]
                carousel = {"type": "carousel", "contents": bubbles}
                
                line_bot_api.reply_message(
                    reply_token,
                    [
                        FlexSendMessage(
                            alt_text="เลือกรุ่นยาง",
                            contents=carousel
                        ),
                        TextSendMessage(
                            text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                            quick_reply=build_quick_reply([
                                ("⬅️ กลับไปเลือกยี่ห้อ", "ยี่ห้อยางรถยนต์"),
                                ("🏠 เมนูหลัก", "แนะนำ"),
                                ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                            ])
                        )
                    ]
                )
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="ไม่พบข้อมูลรุ่นยางในระบบ"),
                )

        # ตรวจสอบการเลือกหมวดหมู่บริการ (ย้ายขึ้นมาก่อนการค้นหายาง)
        elif (category := get_services_by_category(text)):
            print(f"Debug - Found service category: '{text}' with {len(category)} services")
            print(f"Debug - Services: {[s['service_name'] for s in category]}")
            set_user_mode(user_id, "menu")
            flex_content = build_service_list_flex(text, category)
            flex_msg = FlexSendMessage(alt_text=f"บริการหมวด {text}", contents=flex_content)
            quick_buttons = [("🏠 เมนูหลัก", "แนะนำ")]
            quick_reply_msg = TextSendMessage(
                text="เลือกบริการเพิ่มเติมหรือกลับไปเมนูหลัก",
                quick_reply=build_quick_reply_with_extra(quick_buttons),
            )
            line_bot_api.reply_message(reply_token, [flex_msg, quick_reply_msg])

        elif (brand := find_brand_in_text(text)):
            set_user_mode(user_id, "menu")
            models = get_tire_models_by_brand_id(brand["brand_id"])
            if models:
                labels = [m["model_name"] for m in models[:12]]
                bubble = build_selection_list_flex(f"📌 เลือกรุ่นยางของ {brand['brand_name']}", labels)
                line_bot_api.reply_message(
                    reply_token, 
                    [
                        FlexSendMessage(alt_text="เลือกรุ่นยาง", contents=bubble),
                        TextSendMessage(
                            text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                            quick_reply=build_quick_reply([
                                ("🏠 เมนูหลัก", "แนะนำ"),
                                ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                            ])
                        )
                    ]
                )
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text=f"ไม่พบรุ่นของยี่ห้อ {brand['brand_name']} ในระบบ"),
                )

        elif (model := get_tire_model_by_name(text)) or (model := find_model_in_text(text)) or (model := find_model_by_alias(text)):
            # Debug: แสดงข้อมูลรุ่นที่พบ
            print(f"Debug - Found model: {model}")
            print(f"Debug - Model name: {model.get('model_name', '')}")
            print(f"Debug - Brand name: {model.get('brand_name', '')}")
            print(f"Debug - User input: '{text}'")
            set_user_mode(user_id, "menu")
            
            # ดึงข้อมูลยางทั้งหมดของรุ่นนี้
            model_id = model.get("model_id")
            model_name = model.get("model_name", "")
            tires = get_tires_by_model_id(model_id)
            
            print(f"Debug - Found {len(tires)} tires for model {model_name}")
            
            # ถ้าไม่มีข้อมูลยาง ให้ลองดึงข้อมูลยางจากฐานข้อมูลโดยใช้ชื่อรุ่น
            if not tires:
                tires = get_tires_by_model_name(model_name)
                print(f"Debug - Found {len(tires)} tires by model name for {model_name}")
            
            # ถ้ามีข้อมูลยาง ให้ใช้ pagination system
            if tires:
                print(f"Debug - Using pagination system for {len(tires)} tires")
                user_pages[user_id] = {"page": 1, "model_id": model_id}
                send_tires_page(reply_token, user_id)
                return
            
            # ถ้ายังไม่มีข้อมูลยาง ให้สร้างข้อมูลยางตัวอย่าง
            if not tires:
                brand_name = model.get("brand_name", "")
                model_name = model.get("model_name", "")
                tire_category = model.get("tire_category", "ไม่ระบุ")
                
                # สร้างข้อมูลยางตัวอย่างสำหรับรุ่นที่ไม่มีข้อมูล
                sample_tires = create_sample_tires_for_model(model_name, brand_name, tire_category)
                
                if sample_tires:
                    # ใช้ pagination system สำหรับข้อมูลยางตัวอย่าง
                    model_id = model.get("model_id")
                    user_pages[user_id] = {"page": 1, "model_id": model_id}
                    send_tires_page(reply_token, user_id)
                else:
                    # ถ้าไม่สามารถสร้างข้อมูลตัวอย่างได้ ให้แสดงข้อมูลรุ่นยางแบบง่าย
                    bubble = {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"{brand_name} {model_name}",
                                    "weight": "bold",
                                    "size": "xl",
                                    "wrap": True,
                                    "color": "#0B4F6C",
                                },
                                {"type": "separator", "margin": "md"},
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "margin": "md",
                                    "spacing": "sm",
                                    "contents": [
                                        {"type": "text", "text": f"หมวด: {tire_category}"},
                                        {"type": "text", "text": "ไม่พบข้อมูลยางในระบบ", "color": "#FF6B6B"},
                                        {"type": "text", "text": "กรุณาติดต่อร้านเพื่อสอบถามข้อมูลเพิ่มเติม", "size": "sm", "color": "#666666"},
                                    ],
                                },
                            ],
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "style": "link",
                                    "height": "sm",
                                    "action": {
                                        "type": "uri",
                                        "label": "📞 ติดต่อร้าน",
                                        "uri": "tel:044611097"
                                    }
                                }
                            ]
                        }
                    }
                    
                    line_bot_api.reply_message(
                        reply_token,
                        [
                            FlexSendMessage(alt_text=f"ข้อมูลรุ่น {model_name}", contents=bubble),
                            TextSendMessage(
                                text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                                quick_reply=build_quick_reply([
                                    ("⬅️ กลับไปเลือกยี่ห้อ", "ยี่ห้อยางรถยนต์"),
                                    ("🏠 เมนูหลัก", "แนะนำ"),
                                    ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                                ])
                            )
                        ]
                    )
                return

        # จัดการเมื่อเลือกยี่ห้อเฉพาะ
        elif text == "Michelin":
            set_user_mode(user_id, "menu")
            carousel = build_michelin_model_flex()
            line_bot_api.reply_message(
                reply_token,
                [
                    FlexSendMessage(alt_text="เลือกรุ่นยาง Michelin", contents=carousel),
                    TextSendMessage(
                        text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                        quick_reply=build_quick_reply([
                            ("⬅️ กลับไปเลือกยี่ห้อ", "ยี่ห้อยางรถยนต์"),
                            ("🏠 เมนูหลัก", "แนะนำ"),
                            ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                        ])
                    )
                ]
            )

        elif text == "BFGoodrich":
            set_user_mode(user_id, "menu")
            carousel = build_bfgoodrich_model_flex()
            line_bot_api.reply_message(
                reply_token,
                [
                    FlexSendMessage(alt_text="เลือกรุ่นยาง BFGoodrich", contents=carousel),
                    TextSendMessage(
                        text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                        quick_reply=build_quick_reply([
                            ("⬅️ กลับไปเลือกยี่ห้อ", "ยี่ห้อยางรถยนต์"),
                            ("🏠 เมนูหลัก", "แนะนำ"),
                            ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                        ])
                    )
                ]
            )

        elif text == "Maxxis":
            set_user_mode(user_id, "menu")
            carousel = build_maxxis_model_flex()
            line_bot_api.reply_message(
                reply_token,
                [
                    FlexSendMessage(alt_text="เลือกรุ่นยาง Maxxis", contents=carousel),
                    TextSendMessage(
                        text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                        quick_reply=build_quick_reply([
                            ("⬅️ กลับไปเลือกยี่ห้อ", "ยี่ห้อยางรถยนต์"),
                            ("🏠 เมนูหลัก", "แนะนำ"),
                            ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                        ])
                    )
                ]
            )

        else:
            # Debug: แสดงข้อความที่ไม่สามารถจับคู่ได้
            print(f"Debug - No model match found for: '{text}'")
            print(f"Debug - Text length: {len(text)}")
            print(f"Debug - Text type: {type(text)}")
            # ลองค้นหารุ่นยางที่คล้ายกัน
            similar_models = []
            all_brands = get_all_tire_brands()
            for b in all_brands:
                models = get_tire_models_by_brand_id(b["brand_id"])
                for m in models:
                    if text.lower() in m["model_name"].lower() or m["model_name"].lower() in text.lower():
                        similar_models.append(m)
            
            if similar_models:
                # แสดงรุ่นยางที่คล้ายกัน
                bubbles = []
                for model in similar_models[:3]:  # จำกัดไว้ 3 รุ่น
                    brand_name = model.get('brand_name', '')
                    model_name = model.get('model_name', '')
                    
                    # ดึงข้อมูลยางของรุ่นนี้
                    model_id = model.get("model_id")
                    tires = get_tires_by_model_id(model_id)
                    
                    if tires:
                        # สร้าง Flex Message สำหรับแต่ละยาง
                        for tire in tires[:2]:  # จำกัดไว้ 2 รุ่นต่อรุ่นยาง
                            # เพิ่มข้อมูลยี่ห้อใน tire object
                            tire['brand_name'] = brand_name
                            tire_flex = build_tire_flex(tire)
                            bubbles.append(tire_flex)
                            
                            # จำกัดจำนวน bubbles ไม่เกิน 12
                            if len(bubbles) >= 12:
                                break
                    
                    # จำกัดจำนวน bubbles ไม่เกิน 12
                    if len(bubbles) >= 12:
                        break
                    else:
                        # ถ้าไม่มีข้อมูลยาง ให้แสดงข้อมูลรุ่น
                        bubble = {
                            "type": "bubble",
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"{brand_name} {model_name}",
                                        "weight": "bold",
                                        "size": "lg",
                                        "wrap": True,
                                        "color": "#0B4F6C"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"หมวด: {model.get('tire_category', 'ไม่ระบุ')}",
                                        "size": "sm",
                                        "color": "#666666",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "text",
                                        "text": "ไม่พบข้อมูลยางในระบบ",
                                        "size": "sm",
                                        "color": "#FF6B6B",
                                        "margin": "sm"
                                    }
                                ]
                            }
                        }
                        bubbles.append(bubble)
                
                if bubbles:
                    carousel = {"type": "carousel", "contents": bubbles}
                    line_bot_api.reply_message(
                        reply_token,
                        [
                            FlexSendMessage(
                                alt_text="รุ่นยางที่คล้ายกัน",
                                contents=carousel
                            ),
                            TextSendMessage(
                                text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                                quick_reply=build_quick_reply([
                                    ("⬅️ กลับไปเลือกยี่ห้อ", "ยี่ห้อยางรถยนต์"),
                                    ("🏠 เมนูหลัก", "แนะนำ"),
                                    ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                                ])
                            )
                        ]
                    )
                else:
                    line_bot_api.reply_message(
                        reply_token,
                        TextSendMessage(text="ไม่พบรุ่นยางที่คล้ายกัน กรุณาลองใหม่อีกครั้ง")
                    )
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="ไม่พบรุ่นยางที่ตรงกับคำค้นหา กรุณาลองใหม่อีกครั้ง")
                )

        if text.startswith("ยี่ห้อ"):
            # จัดการปุ่มย้อนกลับ
            brand_name = text.replace("ยี่ห้อ", "")
            set_user_mode(user_id, "menu")
            models = get_tire_models_by_brand_id(brand_name)
            if models:
                labels = [m["model_name"] for m in models[:12]]
                bubble = build_selection_list_flex(f"📌 เลือกรุ่นยางของ {brand_name}", labels)
                line_bot_api.reply_message(
                    reply_token, 
                    [
                        FlexSendMessage(alt_text="เลือกรุ่นยาง", contents=bubble),
                        TextSendMessage(
                            text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                            quick_reply=build_quick_reply([
                                ("🏠 เมนูหลัก", "แนะนำ"),
                                ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                            ])
                        )
                    ]
                )
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text=f"ไม่พบรุ่นของยี่ห้อ {brand_name} ในระบบ"),
                )


        elif any(
            w in text
            for w in [
                "ร้านอยู่ไหน",
                "แผนที่",
                "location",
                "พิกัด",
                "ที่อยู่ร้าน",
                "โลเคชัน",
                "ที่ตั้งร้าน",
                "ร้านอยู่ที่ไหน",
                "แผนที่ร้าน",
            ]
        ):
            set_user_mode(user_id, "menu")
            line_bot_api.reply_message(
                reply_token,
                [
                    LocationSendMessage(
                        title="ไทร์พลัส บุรีรัมย์แสงเจริญการยาง",
                        address="365 หมู่ 3 ถนน จิระ ต.ในเมือง อ.เมือง จ.บุรีรัมย์ 31000",
                        latitude=14.9977752,
                        longitude=103.0387382,
                    ),
                    TextSendMessage(
                        text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                        quick_reply=build_quick_reply(
                            [("🏠 เมนูหลัก", "แนะนำ"), ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")]
                        ),
                    ),
                ],
            )

        elif text in ["ติดต่อ", "ติดต่อร้าน", "ติดต่อร้านยาง", "ติดต่อเรา", "เบอร์โทร", "โทรศัพท์"]:
            set_user_mode(user_id, "menu")
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(
                    text="ติดต่อเราได้ที่ ☎️ 044 611 097",
                    quick_reply=build_quick_reply(
                        [("🏠 เมนูหลัก", "แนะนำ"), ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")]
                    ),
                ),
            )

        elif any(word in text.lower() for word in ["เวลาเปิดทำการ", "เปิด", "ร้านเปิดกี่โมง", "ร้านเปิด"]):
            set_user_mode(user_id, "menu")
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(
                    text="เวลาเปิดทำการ 🕗 วันจันทร์ - วันเสาร์ : 08:00 - 17:30",
                    quick_reply=build_quick_reply(
                        [("🏠 เมนูหลัก", "แนะนำ"), ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")]
                    ),
                ),
            )

        elif text in ["ถามเพิ่มเติม", "ถามคำถามอื่น"]:
            set_user_mode(user_id, "free_text")
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(
                    text=(
                        "คุณสามารถพิมพ์คำถามอะไรก็ได้เลยค่ะ เช่น:\n"
                        "- ยางสำหรับรถเก๋ง\n"
                        "- บริการทางร้าน\n"
                        "- โปรโมชั่นเดือนนี้"
                    ),
                    quick_reply=build_quick_reply_with_extra(
                        [
                            ("🏠 เมนูหลัก", "แนะนำ"),
                            ("🚗 เริ่มต้นเลือกยาง", "แนะนำ"),
                            ("🛠️ บริการ", "บริการ"),
                            ("🎉 โปรโมชัน", "โปรโมชัน"),
                            ("📍 ร้านอยู่ที่ไหน", "ร้านอยู่ไหน"),
                            ("📞 ติดต่อร้าน", "ติดต่อร้าน"),
                        ]
                    ),
                ),
            )

        # --- 7) เมนู "โปรโมชัน" ---
        elif "โปร" in text or "promotion" in text.lower() or "โปรโมชัน" in text:
            set_user_mode(user_id, "menu")
            promotions = get_active_promotions()
            if not promotions:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="ขณะนี้ยังไม่มีโปรโมชันค่ะ"),
                )
            else:
                bubbles = [build_promotion_flex(p, i) for i, p in enumerate(promotions[:10])]
                carousel = {"type": "carousel", "contents": bubbles}
                line_bot_api.reply_message(
                    reply_token,
                    [
                        FlexSendMessage(alt_text="โปรโมชัน", contents=carousel),
                        TextSendMessage(
                    text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                            quick_reply=build_quick_reply([
                                ("🏠 เมนูหลัก", "แนะนำ"),
                                ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                            ])
                )
                    ]
                )

        # --- 8) เมนู "บริการ" ---
        elif "บริการ" in text.lower() or "service" in text.lower():
            set_user_mode(user_id, "menu")
            service_categories = get_all_service_categories()
            print(f"Debug - Found {len(service_categories)} service categories: {[cat['category'] for cat in service_categories]}")
            if service_categories:
                bubble = build_selection_list_flex("🛠️ เลือกบริการ", [cat["category"] for cat in service_categories[:12]])
                line_bot_api.reply_message(
                    reply_token, 
                    [
                        FlexSendMessage(alt_text="เลือกบริการ", contents=bubble),
                        TextSendMessage(
                            text="คลิกที่เมนูด้านล่างเพื่อดูเมนูอื่นเพิ่มเติม",
                            quick_reply=build_quick_reply([
                                ("🏠 เมนูหลัก", "แนะนำ"),
                                ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                            ])
                        )
                    ]
                )
            else:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="ขออภัยค่ะ ขณะนี้ยังไม่พบบริการในระบบ"),
                )


        else:
            # Fallback: not matched any quick-reply flow → ask Make
            try:
                make_answer = forward_to_make({
                    "replyToken": reply_token,
                    "userId": user_id,
                    "text": text,
                })
                if make_answer:
                    line_bot_api.reply_message(reply_token, TextSendMessage(text=make_answer))
                # If Make has no answer → remain silent (no reply)
            except Exception as make_err:
                print("❌ Make error:", make_err)
                # Silent on error as well

    except Exception as e:
        print("❌ ERROR:", e)
        try:
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text=f"เกิดข้อผิดพลาด: {str(e)}"),
            )
        except Exception as reply_error:
            print("❌ Failed to send error message:", reply_error)


@handler.add(PostbackEvent)
def handle_postback(event):
    """จัดการ Postback events เช่น การกดปุ่มใน Flex Message"""
    reply_token = event.postback.data
    user_id = event.source.user_id
    
    print(f"Postback received: {reply_token}")
    
    # ตรวจสอบว่าเป็นคำถามตัวอย่างหรือไม่
    if reply_token.startswith("ask_question="):
        question = reply_token.replace("ask_question=", "")
        print(f"User selected example question: {question}")
        
        # เปลี่ยน mode เป็น free_text และส่งคำถามไปยัง Make
        set_user_mode(user_id, "free_text")
        
        # ส่งคำถามไปยัง Make integration
        try:
            make_answer = forward_to_make({
                "replyToken": reply_token,
                "userId": user_id,
                "text": question,
            })
            
            if make_answer:
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text=f"คำถาม: {question}"),
                        TextSendMessage(text=make_answer),
                        TextSendMessage(
                            text="มีคำถามอื่นอีกไหมคะ? หรือพิมพ์ 'แนะนำ' เพื่อกลับไปเมนูหลัก",
                            quick_reply=build_quick_reply([
                                ("🏠 เมนูหลัก", "แนะนำ"),
                                ("❓ ถามคำถามอื่น", "ถามเพิ่มเติม")
                            ])
                        )
                    ]
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="ขออภัยค่ะ ไม่สามารถตอบคำถามได้ในขณะนี้ กรุณาลองใหม่อีกครั้ง")
                )
        except Exception as e:
            print(f"Error calling Make integration: {e}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="ขออภัยค่ะ เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง")
            )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    reply_token = event.reply_token
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(
            text=(
                "ขอบคุณสำหรับสติ๊กเกอร์นะคะ 😊\n"
                "ต้องการให้เราช่วยอะไรดีคะ👇"
            ),
            quick_reply=build_quick_reply(
                [
                    ("🚗 เริ่มต้นเลือกยาง", "แนะนำ"),
                    ("🛠️ บริการ", "บริการ"),
                    ("🎉 โปรโมชัน", "โปรโมชัน"),
                    ("📍 ร้านอยู่ที่ไหน", "ร้านอยู่ไหน"),
                    ("📞 ติดต่อร้าน", "ติดต่อร้าน"),
                ]
            ),
        ),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))