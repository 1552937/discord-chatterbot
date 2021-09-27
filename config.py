from dotenv import load_dotenv
from chatterbot import ChatBot

load_dotenv()


usedChannels = ['ml-chat', 'chat-with-a-bot']


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
bot = ChatBot(
    'Fred',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///database.sqlite3'
)
