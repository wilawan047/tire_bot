import requests
from make_integration import forward_to_make  # ใช้ fallback

CHATPDF_WEBHOOK_URL = "https://hook.eu2.make.com/p5vur0klgafscgd1mq7i8ghiwjm57wn5"

def forward_to_chatpdf(data):
    user_message = str(data.get("text", "")).strip()
    if not user_message:
        return "❌ ไม่มีข้อความส่งไป ChatPDF"

    source_id = "src_cjw53q0gcxYlE668P0ZxZ"
    api_key = "sec_nNEwD1000ioLIYb0HiD7RdUngncuzNut"

    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    payload = {"sourceId": source_id, "messages": [{"role": "user", "content": user_message}]}

    try:
        response = requests.post("https://api.chatpdf.com/v1/chats/message", headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            resp_json = response.json()
            print("🔹 ChatPDF response:", resp_json)  # debug log
            return resp_json.get("content", "ไม่พบคำตอบจากเอกสารค่ะ")
        else:
            return f"❌ Error {response.status_code} จาก ChatPDF: {response.text}"
    except Exception as e:
        print("❌ Exception ส่ง ChatPDF:", e)
        return f"❌ ไม่สามารถเชื่อมต่อ ChatPDF ได้: {e}"
