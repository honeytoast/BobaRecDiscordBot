# SampleDiscordBot-Python  
A simple Discord bot written in Python

## Project structure
```
├── bot.py           -> main entrypoint for the bot
├── requirements.txt 
├── README.md
└── .gitignore
```

## Set up your environment  
python -m venv /path/to/venv  
source /path/to/venv/bin/activate  
pip install -r requirements.txt  

## Create a local .env file (not to be committed)
The .env file should contain your guild ID and your super secret Discord bot token  
.env has already been added to the .gitignore file in this repo.  
```
GUILD_ID=<Your_Guild_ID>  
DISCORD_TOKEN=<Your_DiscordBot_Token>  
```

## Run your bot
python bot.py
