import requests
from make_integration import forward_to_make  # ใช้ fallback

CHATPDF_WEBHOOK_URL = "https://hook.eu2.make.com/p5vur0klgafscgd1mq7i8ghiwjm57wn5"

def forward_to_chatpdf(data):
    """
    ส่งข้อความไป ChatPDF API และ return ข้อความตอบกลับ (string)
    หาก ChatPDF ไม่ตอบ จะ fallback ไป Make
    data: dict {"replyToken": str, "userId": str, "text": str}
    """
    text = str(data.get("text") or "")
    if not text:
        return "❌ ข้อความว่าง ไม่สามารถส่งไป ChatPDF ได้"

    payload = {"messages": [{"role": "user", "content": text}]}

    try:
        response = requests.post(CHATPDF_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            try:
                resp_data = response.json()
                reply_text = resp_data.get("text", "").strip()
                if not reply_text:
                    reply_text = "ไม่พบคำตอบจาก ChatPDF ค่ะ"
            except Exception:
                reply_text = response.text.strip() or "ไม่พบคำตอบจาก ChatPDF ค่ะ"
        else:
            reply_text = f"❌ Error {response.status_code} จาก ChatPDF"
    except Exception as e:
        print(f"❌ ไม่สามารถเชื่อมต่อ ChatPDF: {e}\nFallback ไป Make")
        # นี่คือจุดที่เรียก Make
        reply_text = forward_to_make({
            "replyToken": data.get("replyToken"),
            "userId": data.get("userId"),
            "text": text
        })

    return reply_text
