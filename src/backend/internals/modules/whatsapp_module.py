import os
import requests

AUTH_TOKEN = 'FB_TOKEN'
URL = 'https://graph.facebook.com/v20.0/441387892393551/messages'

def send_whatsapp_message(input_message, phone_number):
    headers = {
        f"Authorization": f"Bearer {os.getenv(AUTH_TOKEN)}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": input_message}
    }

    print(headers)
    print(data)
    response = requests.post(URL, json=data, headers=headers)
    print(response.json())
    return response