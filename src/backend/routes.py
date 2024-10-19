from flask import request, Response

from src.backend.internals.handler.message_handler import handle_whatsapp_message


def setup_routes(app):
    @app.route('/chat', methods=['POST'])
    def chat_response():
        request_body = request.get_json()
        handle_whatsapp_message(request_body)
        return Response(request_body, 200)

    @app.route('/chat', methods=['GET'])
    def chat_verify_webhook():
        # TODO: Verify the token later
        verification_value = request.args.get('hub.challenge')
        return verification_value

    @app.route('/', methods=['GET'])
    def home():
        return Response({}, 200)