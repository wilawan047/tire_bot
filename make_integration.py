import os
import requests
from linebot import LineBotApi
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/p5vur0klgafscgd1mq7i8ghiwjm57wn5"  # ✅ URL จาก Make
if LINE_CHANNEL_ACCESS_TOKEN is None:
    raise ValueError("❌ ต้องตั้งค่า LINE_CHANNEL_ACCESS_TOKEN ใน environment variables ก่อนรัน")



def forward_to_make(data):
    user_message = data.get("text", "").strip()  # ป้องกัน None หรือช่องว่าง
    if not user_message:
        user_message = "❗ ไม่มีข้อความจากผู้ใช้"

    payload = {
        "user_id": data.get("userId", "unknown"),
        "message": user_message
    }

    # 🔹 ส่งข้อความไปยัง Make
    try:
        response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            try:
                make_data = response.json()
                reply_text = make_data.get("text", "").strip()
                # กรองค่า "Accept" หรือข้อความว่าง
                if not reply_text or reply_text.lower() == "accept":
                    reply_text = "ไม่พบคำตอบจาก Make ค่ะ"
            except Exception:
                reply_text = response.text.strip() or "ไม่พบคำตอบจาก Make ค่ะ"
                if reply_text.lower() == "accept":
                    reply_text = "ไม่พบคำตอบจาก Make ค่ะ"
        else:
            reply_text = f"❌ Error {response.status_code} จาก Make"
    except Exception as e:
        reply_text = f"❌ ไม่สามารถเชื่อมต่อ Make ได้: {e}"

    # 🔹 สร้าง Quick Reply คงที่
    quick_items = [
        QuickReplyButton(action=MessageAction(label="🏠 เมนูหลัก", text="แนะนำ")),
        QuickReplyButton(action=MessageAction(label="🚗 เลือกยาง", text="ยี่ห้อยางรถยนต์")),
        QuickReplyButton(action=MessageAction(label="🛠️ บริการ", text="บริการ")),
        QuickReplyButton(action=MessageAction(label="🎉 โปรโมชัน", text="โปรโมชัน")),
        QuickReplyButton(action=MessageAction(label="📍 ร้านอยู่ที่ไหน", text="ร้านอยู่ไหน")),
        QuickReplyButton(action=MessageAction(label="📞 ติดต่อร้าน", text="ติดต่อร้าน")),
    ]

    # 🔹 ส่งข้อความกลับไปยัง LINE
    if "replyToken" in data:
        line_bot_api.reply_message(
            data["replyToken"],
            TextSendMessage(
                text=reply_text,
                quick_reply=QuickReply(items=quick_items)
            )
        )
