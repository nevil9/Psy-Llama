import os
import requests

AUTH_TOKEN = 'FB_TOKEN'
MESSAGE_URL = 'https://graph.facebook.com/v20.0/441387892393551/messages'
MEDIA_URL = 'https://graph.facebook.com/v17.0/'

def send_whatsapp_message(input_message, phone_number):
    headers = {
        f"Authorization": f"Bearer {os.getenv(AUTH_TOKEN)}",
        "Content-Type": "application/json"
    }
    data = {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": phone_number,
      "type": "text",
      "text": {
        "body": input_message
      }
    }

    print(headers)
    print(data)
    response = requests.post(MESSAGE_URL, json=data, headers=headers)
    print(response.json())
    return response

def get_audio_file(file_id):
    headers = {
        f"Authorization": f"Bearer {os.getenv(AUTH_TOKEN)}",
    }

    response = requests.get(MEDIA_URL + file_id, headers=headers)
    print(response.json())
    media_info = response.json()

    # Step 2: Download the media
    download_url = media_info.get('url')
    audio_response = requests.get(download_url, headers=headers)

    # Save the audio file to your local system
    with open('audio_message.wav', 'wb') as audio_file:
        audio_file.write(audio_response.content)

    print("Audio file downloaded successfully.")
    return response

def send_whatsapp_audio_message(file_path):
    upload_url = 'https://graph.facebook.com/v20.0/441387892393551/media'

    headers = {
        f"Authorization": f"Bearer {os.getenv(AUTH_TOKEN)}",
        "Content-Type": "application/json"
    }

    data = {
        'file': file_path,
        'type': 'audio/mpeg',
        'messaging_product': 'whatsapp'
    }

    print(data)
    response = requests.post(upload_url, data=data, headers=headers)
    print('wow')
    print(response.json())
    id = response.json()['id']

    data = {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": "917042504415",
      "type": "audio",
      "audio": {
        "id" : id
      }
    }

    requests.post(MESSAGE_URL, data=data, headers=headers)
    print('done with whatsapp post audio')