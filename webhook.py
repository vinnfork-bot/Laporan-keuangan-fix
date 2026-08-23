from flask import Flask, request
import requests
from parser import parse_pesan
import traceback

app = Flask(__name__)
VERIFY_TOKEN = "WBbth-27122009-11122008"

PHONE_NUMBER_ID = "1261514473711832"

ACCESS_TOKEN = "EAAWDjwt7MzEBSUpeip5CgizZCgeAPqJVdb46ytzJxLtbbyrLUE5AFAmWZB6WrDM6UNDVdDCjT3jCeuKPiWUaZBNUUOuJzz3TLJshROZBkU1KrEgZCfQemD0hkLdzXjpmr3BOQi9CgfljCI5vlwZCQpjJIGtyUJamdHA7jGKl9n7iEalTxg0oPMyZCok00ZBFFVb2TSim6OqWWI3copxP62kLhng9zg6IbNE3sZC2q1rA1NODUKZC4Iw8SovUCLy7RRTEWyR7uZCh2rG8tWexlOCpfdXFQZDZD"

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