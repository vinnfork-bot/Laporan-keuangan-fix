from flask import Flask, request
import requests
from parser import parse_pesan
import traceback

app = Flask(__name__)
VERIFY_TOKEN = "token anda"

PHONE_NUMBER_ID = "id anda"

ACCESS_TOKEN = "akses token anda"
def kirim_pesan(nomor, pesan):

    url = f" link anda"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": nomor,
        "type": "text",
        "text": {
            "body": str(pesan)
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print("Status   :", response.status_code)
    print("Response :", response.text)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("WEBHOOK BERHASIL DI VERIFIKASI")
            return challenge, 200

        print("VERIFIKASI GAGAL")
        return "forbidden", 403
    if request.method == "POST":
        data = request.json

        try:
            value = data["entry"][0]["changes"][0]["value"]

            if "messages" not in value:
                return "EVENT DITERIMA", 200

            message = value["messages"][0]
            nomor = message["from"]
            user_id = nomor
            text = message["text"]["body"].strip().lower()

            print("Nomor : ", nomor)
            print("Pesan : ", text)

            response = parse_pesan(text, nomor)
            print(repr(response))

            if response:
                print("mengirim ke whasapp")
                kirim_pesan(user_id, response)

            else:
                print("respon kosong")
            
        except(KeyError, IndexError, TypeError) as e:
            print("ERORRR", e)
            traceback.print_exc()
        
    return "EVENT DITERIMA", 200

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
        )