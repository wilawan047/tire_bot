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
        print("Make raw response:", response.text)  # แสดง response เพื่อ debug

        if response.status_code == 200:
            try:
                # พยายามแปลงเป็น JSON
                resp_json = response.json()
                return resp_json.get("text") or "ขณะนี้ยังไม่สามารถตอบได้ค่ะ 😅"
            except ValueError:
                # ถ้าไม่ใช่ JSON
                print("❌ Make ส่ง response ที่ไม่ใช่ JSON")
                return "ขณะนี้ยังไม่สามารถตอบได้ค่ะ 😅"
        else:
            return f"❌ Error {response.status_code} จาก Make"
    except requests.RequestException as e:
        return f"❌ ไม่สามารถเชื่อมต่อ Make ได้: {e}"
