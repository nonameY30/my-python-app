from flask import Flask, request, abort
import random
import requests
import os

app = Flask(__name__)

# 建議在 Render 後台設定環境變數，或直接在此貼入你的 Token
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "你的AccessToken")

# 這裡移除原本的 questions 內容，請保留你自己的問題清單
questions = [ ...你的問題清單... ]

user_state = {}

def reply_message(reply_token, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=body)

@app.route("/callback", methods=['POST'])
def callback():
    data = request.json
    if not data or 'events' not in data:
        return 'OK'
    
    events = data['events']
    for event in events:
        if event['type'] != 'message' or 'text' not in event['message']:
            continue
            
        reply_token = event['replyToken']
        user_id = event['source']['userId']
        message = event['message']['text']

        if message == "開始":
            question = random.choice(questions)
            user_state[user_id] = question
            reply_message(reply_token, "📘 題目：\n" + question["q"])
        elif message in ["1","2","3","4"]:
            if user_id in user_state:
                correct = user_state[user_id]["answer"]
                if message == correct:
                    reply_message(reply_token, "✅ 答對了！輸入『開始』下一題")
                    del user_state[user_id] # 答完移除狀態
                else:
                    reply_message(reply_token, f"❌ 答錯，正確答案是 {correct}\n輸入『開始』再來一題")
        else:
            reply_message(reply_token, "輸入『開始』開始測驗")
    return 'OK'

if __name__ == "__main__":
    # Render 會自動分配 Port，所以這裡要讀取環境變數
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
