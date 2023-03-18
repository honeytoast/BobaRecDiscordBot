# SampleDiscordBot-Python  
A simple Discord bot written in Python, which also provides random boba drink recommendations.

## Requirements  
1. A Discord Bot - you can create one for free through the [developer portal](https://discord.com/developers/applications) by creating a new application
2. A Discord Server which you are an admin of
3. python3  
4. virtualenv  
5. (optional) A Google Cloud VM instance to host the bot on 

## Project structure
```
├── bot.py                     -> main entrypoint for the bot  
├──  lib/                      -> contains additional files to support commands  
│   ├── __init__.py  
│   ├── teatime.cfg            -> Context Free Grammar (CFG) file to define potential boba drinks  
│   ├── cfg.py                 -> defines classes for defining a CFG  
│   ├── random_cfg_deriver.py  -> contains logic to randomly derive a string from the cfg  
├── requirements.txt 
├── README.md  
├── sample.jpg                 -> sample of what the bot looks like in Discord
└── .gitignore
```

## Optional (Set up on Google Cloud VM instance)
1. SSH into your VM instance  
2. Install tmux or a terminal multiplexer of your choice  
3. Clone this repository and follow the rest of the instructions to set up  
4. Ensure to run the last step (python bot.py) while you are in a terminal multiplexer session  

## Set up your environment  
python3 -m venv /path/to/venv  
source /path/to/venv/bin/activate  
pip install -r requirements.txt  

## Create a local .env file (not to be committed)
The .env file should contain your guild ID and your super secret Discord bot token.  
.env has already been added to the .gitignore file in this repo.  
```
GUILD_ID=<Your_Guild_ID>  
DISCORD_TOKEN=<Your_DiscordBot_Token>  
```

## Invite your Discord bot to your server
Ensure your bot has the "Send Messages" text permission enabled when you invite it to your server.  
If you don't have a Discord bot yet, follow their [instructions here](https://discord.com/developers/docs/getting-started#creating-an-app) up until you complete the "Installing your App" section.  

## Run your bot
python bot.py

## Sample
![AmberBot, the sample bot responding to commands](/sample.jpg)
