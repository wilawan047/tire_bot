# chatpdf_integration.py
import requests

CHATPDF_WEBHOOK_URL = "https://hook.eu2.make.com/p5vur0klgafscgd1mq7i8ghiwjm57wn5"

def forward_to_chatpdf(data):
    """
    ส่งข้อความไป ChatPDF API และ return ข้อความตอบกลับ (string)
    data: dict {"replyToken": str, "userId": str, "text": str}
    """
    text = data.get("text") or ""
    payload = {"messages": [{"role": "user", "content": text}]}

    try:
        response = requests.post(CHATPDF_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            try:
                chatpdf_data = response.json()
                reply_text = chatpdf_data.get("text", "").strip()
                if not reply_text:
                    reply_text = "ไม่พบคำตอบจาก ChatPDF ค่ะ"
            except Exception:
                reply_text = response.text.strip() or "ไม่พบคำตอบจาก ChatPDF ค่ะ"
        else:
            reply_text = f"❌ Error {response.status_code} จาก ChatPDF"
    except Exception as e:
        reply_text = f"❌ ไม่สามารถเชื่อมต่อ ChatPDF ได้: {e}"

    return reply_text
