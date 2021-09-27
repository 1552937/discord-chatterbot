# bot.py
import asyncio
import concurrent.futures
import os
import re
import subprocess
from sys import version
from os import getenv
import discord
from dotenv import load_dotenv
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pyrebase
import json

import config
load_dotenv()
TOKEN = getenv('TOKEN')
ownerid = int(getenv('ownerID'))
useableChannels = config.usedChannels
startChannel = int(getenv('startChannel'))
email=os.getenv('email')
password=os.getenv('password')
rate = 0
# TODO: add channel for reports
firebaseConfig = json.load(open('firebaseconfig.json'))
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(email, password)
db = firebase.database()

readOnlyBot = config.readOnlyBot
bot2 = config.bot
toTrain = True
trainer = ListTrainer(bot2)

botversion = '0.0.0'


client = discord.Client(activity=discord.Activity(type=discord.ActivityType.playing, name="-chatbot help"))


newlineSequence = ' $NEW;LINE() '

def respond(a):
    try:
        bot_input = readOnlyBot.get_response(a)
    except:
        bot_input = "You broke the chatbot. Sorry for the inconvenience. "
    return str(bot_input)


def train(a, b):
    trainer.train([a, b])


@client.event
async def on_ready():
    channel = await client.fetch_channel(startChannel)
    await channel.send('Chatbot version '+str(botversion)+' connected to discord. ')
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    global rate
    global toTrain
    global user
    user = auth.refresh(user['refreshToken'])
    
    if message.author.id == client.user.id or message.author.bot:
        return
    if message.is_system():
        return

    if message.content.lower().startswith('-load'):
        a = await message.channel.send('Server load at ??%')
        load = subprocess.check_output(
            ['sh', 'bin/load.sh']).decode('utf-8').strip()
        await a.edit(content='Server load at '+str(load)+'%')

    if message.content.lower().startswith('-uptime'):
        up = subprocess.check_output(['uptime', '-p']).decode('utf-8').strip()
        await message.channel.sent('Server ' + up)

    if message.content.lower().startswith('-chatbot help'):
        await message.channel.send('Chatbot Commands:\n-chatbot help\n-load\n-uptime\n-info\n-train - trains the chatbot with the 2 statements you put in. Example of use: "-train -trigger Hi -response Hello"')
        return

    if message.content.lower().startswith('-info'):

        up = subprocess.check_output(['uptime', '-p']).decode('utf-8').strip()
        deviceName = subprocess.check_output(
            ['hostname']).decode('utf-8').strip()
        kernelVersion = subprocess.check_output(
            ['uname', '-r']).decode('utf-8').strip()
        # get uptime, device name, kernel version,
        load = '??'
        channels = ''
        for channel in message.guild.channels:
            if channel.name in useableChannels:
                channels = channels + channel.name+', '
        a = await message.channel.send('This is ' + client.user.name + ' running on ' + deviceName + '\n It has an uptime of ' + up + '\n' + 'It is running version ' + kernelVersion + ' of the linux kernel and version ' + botversion + ' of the chatbot.' + '\n' + 'In ' + message.guild.name + ' the bot will speak in the following channels: ' + channels + '\nThe bot is in '+str(len(client.guilds))+' servers. \nCpu load is at ' + load + '%')
        # send primary message
        load = subprocess.check_output(
            ['sh', 'bin/load.sh']).decode('utf-8').strip()
        await a.edit(content='This is ' + client.user.name + ' running on ' + deviceName + '\n It has an uptime of ' + up + '\n' + 'It is running version ' + kernelVersion + ' of the linux kernel and version ' + botversion + ' of the chatbot.' + '\n' + 'In ' + message.guild.name + ' the bot will speak in the following channels: ' + channels + '\nThe bot is in '+str(len(client.guilds))+' servers. \nCpu load is at ' + load + '%')
        # check and update message with server load

    
    

    if not message.channel.name in useableChannels:
        return
    loop = asyncio.get_running_loop()
    if message.content.lower().startswith('-train'):
        
        if not '-trigger' in message.content:
            await message.channel.send('You are missing your -trigger argument.  ')
            # check to see if trigger is present
            return

        if not '-response' in message.content:
            await message.channel.send('Sorry it appears that you are missing your -response argument. ')
            # check to see if response is present
            return

        part1re = re.search('-trigger(.*)-response', message.content).group(0)
        part1 = part1re[8:].replace('-response', '')
        part1 = part1.replace("\n", newlineSequence)
        # trim the regex statement to the necessary part

        part2 = message.content.partition('-response')[2]
        part2 = part2.replace("\n", newlineSequence)
        # get the part after -response
        print(message.content.partition('-response'))
        if len(part1.replace(' ', '')) < 2:
            await message.channel.send('Your trigger looks like its either all spaces or has like 1 character in it. Maybe try again with more real charachters?')
            return
            # make sure it isnt all spaces or 1 letter
        if len(part2.replace(' ', '')) < 2:
            await message.channel.send('Your response looks like its either all spaces or has like 1 character in it. Maybe try again with more real charachters?')
            return
            # make sure it isnt all spaces or 1 letter
        a = await message.channel.send('Training: \n' + part1.replace(newlineSequence, "/n") + '\nWith: \n' + part2.replace(newlineSequence, "/n"))

        with concurrent.futures.ProcessPoolExecutor() as pool:
            await loop.run_in_executor(pool, train, part1, part2)
        await a.edit(content='Trained: \n' + part1.replace(newlineSequence, "/n") + ' \nWith: \n' + part2.replace(newlineSequence, "/n"))
        return
    if message.content.lower().startswith('-'):
        return
    a = await message.reply('Processing:', mention_author=False)
    
    if(rate == None):
        rate = 1
    elif rate >= 4:
        await a.edit(content='Your channel has too many messages waiting to be processed. Your input has been ignored. ')
        return
    else:
        rate = rate + 1
    
        
    userContent = message.content
    if(message.attachments):
        url = message.attachments[0].url
        userContent = userContent + ' ' + url
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, respond, userContent)
        await a.edit(content=result.replace(newlineSequence, "/n"))
        lastResponse = db.child('channels').child(str(message.channel.id)).child('lastMessage').get(user['idToken']).val()
        if lastResponse==None:
            totrain = False
        else:
            totrain = True
        trained = loop.run_in_executor(pool, train, lastResponse, userContent)
        value = db.child('channels').child(message.channel.id).child('processing').get(user['idToken']).val()
        rate = rate-1
        if(not (result == "You broke the chatbot. Sorry for the inconvenience. " and totrain == False)):
            db.child('channels').child(str(message.channel.id)).child('lastMessage').set(result, user['idToken'])

        
client.run(TOKEN)
