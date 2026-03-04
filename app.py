from flask import Flask, request, abort
import random
import requests
import os

app = Flask(__name__)

# 請把下方引號內的文字換成你真正的 Token
CHANNEL_ACCESS_TOKEN = "你的AccessToken"

questions = [
    {
        "q": "死亡職災幾小時內通報？\n1.8小時\n2.24小時\n3.48小時\n4.72小時",
        "answer": "1"
    },
    {
        "q": "堆高機載物架最多載幾人？\n1.1人\n2.2人\n3.不可載人\n4.3人",
        "answer": "3"
    },
    {
        "q": "職安委員會多久開會一次？\n1.每月\n2.每2個月\n3.每6個月\n4.每3個月",
        "answer": "4"
    }
]

user_state = {}

def reply_message(reply_token, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "replyToken": reply_token,
        "messages":
    }
    requests.post("https://api.line.me", headers=headers, json=body)

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
        message = event['message']

        if message == "開始":
            question = random.choice(questions)
            user_state[user_id] = question
            reply_message(reply_token, "📘 題目：\n" + question["q"])
        elif message in ["1","2","3","4"]:
            if user_id in user_state:
                correct = user_state[user_id]["answer"]
                if message == correct:
                    reply_message(reply_token, "✅ 答對了！輸入『開始』下一題")
                    del user_state[user_id]
                else:
                    reply_message(reply_token, f"❌ 答錯，正確答案是 {correct}\n輸入『開始』再來一題")
        else:
            reply_message(reply_token, "輸入『開始』開始測驗")
    return 'OK'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
