import requests
def forward_to_make(data):
    user_message = str(data.get("text", "")).strip() or "❗ ไม่มีข้อความจากผู้ใช้"

    url = "https://hook.eu2.make.com/p5vur0klgafscgd1mq7i8ghiwjm57wn5"
    payload = {
        "user_id": data.get("userId", "unknown"),
        "message": user_message
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            # สมมติ Make ตอบ JSON
            return response.json().get("text", "ขณะนี้ยังไม่สามารถตอบได้ค่ะ 😅")
        else:
            return f"❌ Error {response.status_code} จาก Make"
    except Exception as e:
        return f"❌ ไม่สามารถเชื่อมต่อ Make ได้: {e}"