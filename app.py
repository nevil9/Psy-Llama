from flask import Flask
import os
from dotenv import load_dotenv
from flask_cors import CORS

from src.backend.routes import setup_routes

load_dotenv()
app = Flask(__name__)
CORS(app)
setup_routes(app)

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=os.environ.get("PORT", 5000))
