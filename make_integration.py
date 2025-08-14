import requests

def forward_to_make(data):
    user_message = data.get("text", "").strip()  # ป้องกัน None หรือช่องว่าง

    if not user_message:
        user_message = "❗ ไม่มีข้อความจากผู้ใช้"

    url = "https://hook.eu2.make.com/p5vur0klgafscgd1mq7i8ghiwjm57wn5"  # URL จาก Make
    payload = {
        "user_id": data.get("userId", "unknown"),
        "message": user_message
    }
    requests.post(url, json=payload)
