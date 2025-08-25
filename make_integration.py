import requests

MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/p5vur0klgafscgd1mq7i8ghiwjm57wn5"

def forward_to_make(data):
    """
    ส่งข้อความไป Make API และ return ข้อความตอบกลับ (string)
    data: dict {"replyToken": str, "userId": str, "text": str}
    """
    text = data.get("text") or ""  # ป้องกัน undefined / None

    payload = {
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ]
    }

    try:
        response = requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            try:
                make_data = response.json()
                reply_text = make_data.get("text", "").strip()
                if not reply_text or reply_text.lower() == "accept":
                    reply_text = "ไม่พบคำตอบจาก Make ค่ะ"
            except Exception:
                reply_text = response.text.strip() or "ไม่พบคำตอบจาก Make ค่ะ"
        else:
            reply_text = f"❌ Error {response.status_code} จาก Make"
    except Exception as e:
        reply_text = f"❌ ไม่สามารถเชื่อมต่อ Make ได้: {e}"

    return reply_text
