import requests
from make_integration import forward_to_make  # ใช้ fallback

CHATPDF_WEBHOOK_URL = "https://hook.eu2.make.com/p5vur0klgafscgd1mq7i8ghiwjm57wn5"

def forward_to_chatpdf(data):
    user_message = str(data.get("text", "")).strip()
    if not user_message:
        return "❌ ไม่มีข้อความส่งไป ChatPDF"

    source_id = "src_cjw53q0gcxYlE668P0ZxZ"
    api_key = "sec_awHqhVhMOa8NMeEgPp0Go"

    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    payload = {"sourceId": source_id, "messages": [{"role": "user", "content": user_message}]}

    try:
        response = requests.post("https://api.chatpdf.com/v1/chats/message", headers=headers, json=payload, timeout=10)
        print(f"🔹 ChatPDF response status: {response.status_code}")
        print(f"🔹 ChatPDF response text: {response.text}")
        
        if response.status_code == 200:
            try:
                resp_json = response.json()
                print("🔹 ChatPDF response JSON:", resp_json)  # debug log
                
                # ตรวจสอบว่า response มี data หรือไม่
                if isinstance(resp_json, dict):
                    content = resp_json.get("content")
                    if content:
                        return content
                    else:
                        return "ไม่พบคำตอบจากเอกสารค่ะ"
                else:
                    return "รูปแบบข้อมูลตอบกลับไม่ถูกต้องค่ะ"
            except ValueError as json_err:
                print(f"❌ JSON decode error: {json_err}")
                return "ไม่สามารถประมวลผลข้อมูลตอบกลับได้ค่ะ"
        else:
            error_msg = f"❌ Error {response.status_code} จาก ChatPDF"
            try:
                error_detail = response.json().get("message", response.text)
                return f"{error_msg}: {error_detail}"
            except:
                return f"{error_msg}: {response.text}"
    except requests.RequestException as e:
        print(f"❌ Request exception ส่ง ChatPDF: {e}")
        return f"❌ ไม่สามารถเชื่อมต่อ ChatPDF ได้: {e}"
    except Exception as e:
        print(f"❌ General exception ส่ง ChatPDF: {e}")
        return f"❌ เกิดข้อผิดพลาด: {e}"
