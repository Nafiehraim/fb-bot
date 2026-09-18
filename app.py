import requests
from flask import Flask, request
import google.generativeai as genai
import os

app = Flask(__name__)

# حط المفاتيح ديالك هنا - بدلهم بالمفاتيح الحقيقية
GEMINI_KEY = "AQ.Ab8RN6JxbQuy2iAMhDaxWk0UaeElNM2o8Mr3nY-3dcrjUlNRSw"
PAGE_TOKEN = "EAAZCKMfvowWsBSr3Lk5bzqu6pwYGBnfNsvHxds7JpH2wZBRARJXA8OgpVOrZB0YW9GFtZAygCiKRAB5cK3J6FgN14e9UyJWi7QQrLE9WMfqotodI6uxs9GqhG8feZCufQgPsXjBjN7GgmU3JLJ9JfffmEwl6aGlF1EL4pjf0O5xfNDBXJ6DAuuXzzbRwq66rPpkvuGYfLoWdQxu22YTqvbbkNHQQBXGwIKRZAAzgKIE3nKZCjJAaFY89e4FJ6fkOQ0rcqNA7NWZCGYEm2A36pIi0b8IAoFG44CPasoFevx6C918AY1wg667YJCAyI6ZBg6mAs1doW2hRYAEzF"
VERIFY_TOKEN = "123456"

genai.configure(api_key=GEMINI_KEY)

# الموديل الجديد 2.5
model = genai.GenerativeModel('gemini-2.5-flash')

def send_message(sender_id, text):
    if len(text) > 1900:
        text = text[:1900] + "..."
    
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_TOKEN}"
    data = {
        "recipient": {"id": sender_id},
        "message": {"text": text}
    }
    try:
        requests.post(url, json=data)
    except Exception as e:
        print(f"Send Error: {e}")

# باش Render يعرف بلي السيرفر خدام
@app.route('/')
def home():
    return "البوت خدام! Bot is running!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed", 403
    
    if request.method == 'POST':
        data = request.json
        if 'entry' in data:
            for entry in data['entry']:
                for msg in entry.get('messaging', []):
                    if 'message' in msg and 'text' in msg['message']:
                        user_id = msg['sender']['id']
                        user_text = msg['message']['text']
                        print(f"جات رسالة: {user_text}")
                        try:
                            response = model.generate_content(user_text)
                            send_message(user_id, response.text)
                        except Exception as e:
                            print(f"Gemini Error: {e}")
                            send_message(user_id, "سمح ليا، وقع شي مشكل دابا، عاود جرب من شوية")
        return "ok", 200

if __name__ == '__main__':
    # هادي مهمة بزاف باش يخدم فـ Gethop / Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
