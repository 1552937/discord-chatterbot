# discord-chatterbot
A simple discord bot using chatterbot. Written in python. 
This is a really shitty bot and is very inefficient. Please do not use it without making some major modifications. 

##Setup instructions: 
```bash
git clone git@github.com:1552937/discord-chatterbot.git
cd discord-chatbot
```
Sorry I haven't written my requirements.txt yet. Once I do that I can add it here. 

Login to firebase.google.com and create a new database, then go to the realtime database section and make one of those. 
Add a webapp to the project and copy the information from the configuration section into firebaseconfig.json
Enable email authentication for the project and make a new user with your desired username and password. 
Copy the username and password into the .env file. 
Open https://discord.com/developers/applications and create a new application. Go to the bot section and create a bot. Copy the bot token into .env.

Run the chatbot.py file. It should work. If not sorry let me know and I can fix it. 
