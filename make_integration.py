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

        # ถ้าเป็น JSON
        try:
            resp_json = response.json()
            return resp_json.get("text") or "ขณะนี้ยังไม่สามารถตอบได้ค่ะ 😅"
        except ValueError:
            # ถ้าไม่ใช่ JSON → ใช้ข้อความตรง ๆ
            return response.text or "ขณะนี้ยังไม่สามารถตอบได้ค่ะ 😅"

    except requests.RequestException as e:
        print(f"❌ ไม่สามารถเชื่อมต่อ Make ได้: {e}")
        return "ขณะนี้ยังไม่สามารถตอบได้ค่ะ 😅"
