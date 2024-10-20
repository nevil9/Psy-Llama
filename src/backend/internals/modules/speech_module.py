import requests
import os
import base64

def convert_audio_to_text():
    url = "https://api.sarvam.ai/speech-to-text-translate"

    # Prepare the form data
    payload = {
        'model': 'saaras:v1',  # Mandatory model parameter
    }

    # Open the audio file
    files = {
        'file': ('audio_message.wav', open('audio_message.wav', 'rb'), 'audio/wav')   # The file parameter (required by API)
    }

    headers = {
        f"api-subscription-key": f"{os.getenv('SARVAM_AUTH_TOKEN')}",
    }

    # Send the request with the audio file and data
    response = requests.post(url, data=payload, files=files, headers=headers)
    print(response.json())
    response = response.json()
    return response['transcript'], response['language_code']

def get_spoken_response(text, language):
    url = "https://api.sarvam.ai/text-to-speech"
    headers = {
        f"api-subscription-key": f"{os.getenv('SARVAM_AUTH_TOKEN')}",
    }

    payload = {
        "inputs": [text],
        "target_language_code": language,
        "speaker": "meera",
        "pitch": 0,
        "pace": 1.65,
        "loudness": 1.5,
        "speech_sample_rate": 8000,
        "enable_preprocessing": True,
        "model": "bulbul:v1"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    response_base64 = response.json()['audios'][0]
    audio_data = base64.b64decode(response_base64)

    # Write the binary data to a .wav file
    with open('text_to_speech.mpeg', 'wb') as wav_file:
        wav_file.write(audio_data)

    print('done written the text to speech data')
    return 'text_to_speech.mpeg'