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
        print("Make raw response:", response.text)  # debug

        try:
            resp_json = response.json()
            # ✅ ถ้ามี text จริงเท่านั้น
            if resp_json.get("text"):
                return resp_json["text"]
            else:
                return None  # ไม่มี text → ไม่ตอบอะไร
        except ValueError:
            # ถ้าไม่ใช่ JSON → ไม่ตอบอะไร
            return None

    except requests.RequestException as e:
        print(f"❌ ไม่สามารถเชื่อมต่อ Make ได้: {e}")
        return None
