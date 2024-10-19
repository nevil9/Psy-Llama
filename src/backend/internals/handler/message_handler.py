from src import chatbot_instance
from src.backend.internals.modules.translation_module import translate_text_to_english
from src.backend.internals.modules.whatsapp_module import send_whatsapp_message


def handle_whatsapp_message(body: dict):
    print('handling whatsapp message')
    if body.get('entry')[0].get('changes')[0].get('value').get('messages')[0].get('type') == 'text':
        final_text_response = handle_text_message(body)

    else:
        final_text_response = handle_audio_message(body)

    # TODO: do error handling if any
    send_whatsapp_message(final_text_response, body.get('entry')[0].get('changes')[0].get('value').get('messages')[0].get('from'))
    return


def handle_text_message(body: dict):
    # translated_text,language = translate_text_to_english(body.get('entry')[0].get('messages')[0].get('text').get('body'))
    psi_llm_response = chatbot_instance.respond(body.get('entry')[0].get('changes')[0].get('value').get('messages')[0].get('text').get('body'))
    # reverse_translation = translate_text_to_language(psi_llm_response, language)
    return psi_llm_response

def handle_audio_message(body: dict):
    return ''

def rajan_fn():
    pass