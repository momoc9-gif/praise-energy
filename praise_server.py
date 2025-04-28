from flask import Flask, request, render_template_string
import openai
import requests

app = Flask(__name__)

# API 키
openai.api_key = "너의-OPENAI-API-KEY"
pushover_user_key = "너의-USER-KEY"
pushover_app_token = "너의-APP-TOKEN"

coin_balance = 0

html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>마음에너지 충전봇</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style='text-align: center; margin-top: 100px;'>
    <h1>나한테 말 걸어봐!</h1>
    <form action="/energy" method="post">
        <input type="text" name="message" placeholder="예: 나 오늘 힘들었어" style='width: 80%; height: 40px; font-size: 18px;'><br><br>
        <input type="submit" value="에너지 충전!" style='width: 60%; height: 50px; font-size: 20px;'>
    </form>
    <br><br>
    <h3 style="font-size: 18px;">현재 코인: {{ coin }} 개</h3>
</body>
</html>
"""

def generate_response(user_message):
    system_prompt = "너는 친한 친구처럼 다정하게, 공감하고 격려해주면서 대답하는 마음에너지 충전봇이야. 상대방의 기분을 존중하고, 따뜻한 말로 힘을 북돋아줘. 한 번에 2~3문장 정도, 짧고 따뜻하게 답해줘. 너무 딱딱하거나 공식적으로 말하지 말고, 편하게 대화하듯 답변해."

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response['choices'][0]['message']['content']

def send_push_notification(message):
    url = "https://api.pushover.net/1/messages.json"
    payload = {
        "token": pushover_app_token,
        "user": pushover_user_key,
        "message": message
    }
    requests.post(url, data=payload)

@app.route('/energy', methods=['GET', 'POST'])
def energy():
    global coin_balance

    if request.method == 'POST':
        user_message = request.form['message']
        reply_message = generate_response(user_message)

        coin_balance += 1

        full_message = f"{reply_message}\n\n(오늘도 코인 +1! 총 {coin_balance}개)"

        send_push_notification(full_message)
        return render_template_string(html_form, coin=coin_balance)

    return render_template_string(html_form, coin=coin_balance)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
