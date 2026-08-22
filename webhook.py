from flask import Flask, request
import requests
from parser import parse_pesan
import traceback

app = Flask(__name__)
VERIFY_TOKEN = "WBbth-27122009-11122008"

PHONE_NUMBER_ID = "1261514473711832"

ACCESS_TOKEN = "EAAWDjwt7MzEBSbJTT6QL7cOyWy53hbkwJuaqG4WJy5akn13Icm7gONM06tIzsSWlVJNLZAOSl9jfC1TVOHQL0JJpI8eEOZADQ12bhdgp6HebK4unhKJQNtAVZAhyuMe4Jguiu1RIKTLEVeSGy55nTr9IFDHuVq9hoGHeYPHLyU4LytZCFnmnsxa0RZAbD2gZBJdl9nXYhtfCiKw7ac5wp6lxQXZA4gXgfx0qaF4ZAtMiVqMNqeNfKrMJMCUr8nvSA0rcQrSFiORfkJlyKPmxnevn"

def kirim_pesan(nomor, pesan):

    url = f"https://graph.facebook.com/v25.0/1261514473711832/messages"

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