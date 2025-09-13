import requests

def forward_to_make(data):
    user_message = str(data.get("text", "")).strip() or "❗ ไม่มีข้อความจากผู้ใช้"

    url = "https://hook.eu2.make.com/7qkudqz0kbrzhfgv6gc27qidw2xvz63p"
    payload = {
        "user_id": data.get("userId", "unknown"),
        "message": user_message
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        print("Make raw response:", response.text)  # debug

        # ตรวจสอบว่า Make ตอบ "Queue is full" หรือไม่
        if response.text.strip() == "Queue is full.":
            print("⚠️ Make queue is full, providing fallback response")
            fallback_message = (
                "ขออภัยค่ะ ระบบตอบคำถามกำลังมีผู้ใช้จำนวนมากในขณะนี้\n"
                "กรุณาลองใหม่อีกครั้งในสักครู่ หรือติดต่อร้านโดยตรงที่ ☎️ 044 611 097"
            )
            return fallback_message
        
        # ตรวจสอบว่า Make ตอบ "Accepted" หรือไม่
        if response.text.strip() == "Accepted":
            print("⚠️ Make returned 'Accepted', providing fallback response")
            fallback_message = (
                "ขออภัยค่ะ ระบบตอบคำถามกำลังประมวลผลคำถามของคุณ\n"
                "กรุณารอสักครู่ หรือติดต่อร้านโดยตรงที่ ☎️ 044 611 097"
            )
            return fallback_message

        try:
            resp_json = response.json()
            # ✅ ถ้ามี text จริงเท่านั้น
            if resp_json.get("text"):
                # ส่งคำตอบจาก Make โดยไม่เพิ่มข้อความออกจากเมนู
                make_answer = resp_json["text"]
                return make_answer
            else:
                return None  # ไม่มี text → ไม่ตอบอะไร
        except ValueError:
            # ถ้าไม่ใช่ JSON → ไม่ตอบอะไร
            return None

    except requests.RequestException as e:
        print(f"❌ ไม่สามารถเชื่อมต่อ Make ได้: {e}")
        fallback_message = (
            "ขออภัยค่ะ ไม่สามารถเชื่อมต่อระบบตอบคำถามได้ในขณะนี้\n"
            "กรุณาติดต่อร้านโดยตรงที่ ☎️ 044 611 097"
        )
        return fallback_message
