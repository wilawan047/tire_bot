import requests
def forward_to_chatpdf(data):
    user_message = data.get("text", "").strip()
    
    if not user_message:
        raise Exception("❗ ไม่มีข้อความ (text) ที่จะส่งไปยัง ChatPDF")

    source_id = "src_cjw53q0gcxYlE668P0ZxZ"
    api_key = "sec_nNEwD1000ioLIYb0HiD7RdUngncuzNut"

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "sourceId": source_id,
        "messages": [
            {
                "role": "user",
                "content": user_message  # ✅ ต้องเป็น string ที่ไม่ว่าง
            }
        ]
    }

    response = requests.post(
        "https://api.chatpdf.com/v1/chats/message",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json().get("content", "ไม่พบคำตอบจากเอกสารค่ะ")
    else:
        raise Exception(response.text)
