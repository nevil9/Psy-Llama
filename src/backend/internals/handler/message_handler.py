from src.backend.internals.modules.speech_module import convert_audio_to_text, get_spoken_response
from src.backend.internals.modules.whatsapp_module import send_whatsapp_message, get_audio_file, \
    send_whatsapp_audio_message
from src.backend.internals.orchestra_refactored_module import chatbot_instance
from flask import request, Response




def handle_whatsapp_message(body: dict):
    handle_text_message(body) if body['entry'][0]['changes'][0]['value']['messages'][0]['type'] == 'text' else handle_audio_message(body)

def handle_text_message(body: dict):
    # translated_text,language = translate_text_to_english(body.get('entry')[0].get('messages')[0].get('text').get('body'))
    psi_llm_response = chatbot_instance.respond(body.get('entry')[0].get('changes')[0].get('value').get('messages')[0].get('text').get('body'))
    # reverse_translation = translate_text_to_language(psi_llm_response, language)
    send_whatsapp_message(psi_llm_response, '917042504415')

def handle_audio_message(body: dict):
    print('handling audio message')
    print(body['entry'][0]['changes'][0]['value']['messages'][0]['audio']['id'])
    get_audio_file(body['entry'][0]['changes'][0]['value']['messages'][0]['audio']['id'])
    text,language = convert_audio_to_text()

    text = chatbot_instance.respond(text)
    # if not language:
    send_whatsapp_message(text, '917042504415')

    # else:
        # spoken_response_path = get_spoken_response(text, language)
        # if spoken_response_path:
        #     send_whatsapp_audio_message(spoken_response_path)

    print('done')

def rajan_fn():
    pass