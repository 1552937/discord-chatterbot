from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
bot = ChatBot(
    'Fred',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///databaseubuntu.sqlite3'
)
trainer = ChatterBotCorpusTrainer(bot)
trainer.train(
    "chatterbot.corpus.english.ai",
    "chatterbot.corpus.english.computers",
    "chatterbot.corpus.english.conversations",
    "chatterbot.corpus.english.botprofile",
    "chatterbot.corpus.english.emotion",
    "chatterbot.corpus.english.gossip",
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.health",
    "chatterbot.corpus.english.history",
    "chatterbot.corpus.english.humor",
    "chatterbot.corpus.english.literature",
    "chatterbot.corpus.english.money",
    "chatterbot.corpus.english.movies",
    "chatterbot.corpus.english.politics",
    "chatterbot.corpus.english.psychology",
    "chatterbot.corpus.english.science",
    "chatterbot.corpus.english.sports"
    "chatterbot.corpus.english.trivia"
   "chatterbot.corpus.english"
)

