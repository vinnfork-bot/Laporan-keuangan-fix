from flask import Flask, request
import requests
from parser import parse_pesan
import traceback
from config import ACCESS_TOKEN, PHONE_NUMBER_ID
from export_excel import *

app = Flask(__name__)
VERIFY_TOKEN = "WBbth-27122009-11122008"

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

def upload_file(file_path):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/media"

    print("UPLOAD URL :", url)

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    try:
        with open(file_path, "rb") as file:
            files = {
                "file": (
                    file_path.split("\\")[-1],
                    file,
                    mime_type,
                )
            }
            data = {
                "messaging_product": "whatsapp"
            }

            response = requests.post(
                url,
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )

        print("UP STATUS : ", response.status_code)
        print("UPLOAD RESPONSE :", response.text)

        if response.status_code not in (200, 201):
            return None

        hasil = response.json()
        media_id = hasil.get("id")

        if not media_id:
            print("UPLOAD GAGAL: response tidak punya id", hasil)
            return None

        return media_id

    except FileNotFoundError:
        print("file tidak ada ", file_path)
        return None

    except Exception as e:
        print("error upload : ", e)
        traceback.print_exc()
        return None

def kirim(user_id, media_id, nama_file, nomor):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": nomor,
        "type": "document",
        "document": {
            "id": media_id,
            "filename": nama_file,
            "caption": "📊 rekap transaksi"
        }
    }

    response = requests.post(
        url,
        headers = headers,
        json = payload
    )
    print("KIRIM FILE STATUS   :", response.status_code)
    print("KIRIM FILE RESPONSE :", response.text)
    return response
    

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

    file_path = "export\\08-2026.xlsx"

    media_id = upload_file(file_path)

    print("MEDIA ID :", media_id)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
