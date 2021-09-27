import chatterbot
# import asyncio
# import concurrent.futures
# import os
# import re
# import subprocess
import time
# from sys import version
# from threading import Thread
import flask
from flask import Flask
# import discord
from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
# from dotenv import load_dotenv
import sys
# statement = sys.argv[1]
readOnlyBot = ChatBot(
    'Fred',
    read_only=True,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///database.sqlite3'
)
# print(readOnlyBot.get_response(statement))

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    # print(flask.request.args.get('input'))
    t1=time.time()
    a = readOnlyBot.get_response(flask.request.args.get('input'))
    print(time.time()-t1)
    return str(a)

if __name__ == '__main__':
    app.run(port = 5000)