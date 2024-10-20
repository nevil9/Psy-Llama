from flask import Flask
import os
from dotenv import load_dotenv
from flask_cors import CORS

from flask import request, Response
import threading

from src.backend.internals.handler.message_handler import handle_whatsapp_message

load_dotenv()
app = Flask(__name__)
CORS(app)

id_set = set()

@app.route('/chat', methods=['POST'])
def chat_response():
	print('post request made ')
	request_body = request.get_json()
	print(request_body)
	if 'statuses' in request_body['entry'][0]['changes'][0]['value'].keys():
		print("this is a sent msg")
		return Response(request_body, 200)

	if request_body['entry'][0]['changes'][0]['value']['messages'][0]['id'] in id_set:
		return Response(request_body, 200)

	else:
		id_set.add(request_body['entry'][0]['changes'][0]['value']['messages'][0]['id'])


	print(request_body)
	thread = threading.Thread(target=handle_whatsapp_message, args=(request_body,))
	thread.start()
	print('post request!')
	# Immediately return response
	return Response("Processing started", status=200)

@app.route('/chat', methods=['GET'])
def chat_verify_webhook():
	# TODO: Verify the token later
	verification_value = request.args.get('hub.challenge')
	return Response(verification_value, 200)

@app.route('/', methods=['GET'])
def home():
	return Response({}, 200)


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=os.environ.get("PORT", 5000))
