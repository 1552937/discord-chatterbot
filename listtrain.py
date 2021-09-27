from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
filename = "trainingdoc.txt"
bot = ChatBot(
    'Norman',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///database.sqlite3'
)
from chatterbot.trainers import ListTrainer

conversation = []
import os
with open(filename) as file:
    for line in file: 
        line = line.strip() #or some other preprocessing
        conversation.append(line)
        print(line)
trainer = ListTrainer(bot)
trainer.train(conversation)

