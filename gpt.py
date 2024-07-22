from flask import Flask, request, jsonify, render_template, Blueprint
from flask_restful import Api
from flask_cors import CORS
from chat_api import *


app = Flask(__name__)
api = Api(app)
CORS(app)

#chat api
api.add_resource(QueryChat, "/gpt/chat/push/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3500)
