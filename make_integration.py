# make_integration.py
import requests

# URL ของ Make Webhook จริง (หรือ ChatPDF สำหรับ fallback)
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/p5vur0klgafscgd1mq7i8ghiwjm57wn5"

def forward_to_make(data):
    text = str(data.get("text") or "")
    if not text:
        return "❌ ข้อความว่าง ไม่สามารถส่งไป Make ได้"

    payload = {"messages": [{"role": "user", "content": text}]}

    try:
        response = requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            try:
                resp_data = response.json()
                reply_text = resp_data.get("text", "").strip() or "ขณะนี้ยังไม่สามารถตอบได้ค่ะ 😅"
            except Exception:
                reply_text = response.text.strip() or "ขณะนี้ยังไม่สามารถตอบได้ค่ะ 😅"
        else:
            reply_text = f"❌ Error {response.status_code} จาก Make"
    except Exception as e:
        reply_text = f"❌ ไม่สามารถเชื่อมต่อ Make ได้: {e}"

    return reply_text

