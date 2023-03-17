import os
import sys
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


"""
Whenever the connection is ready
"""
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, id=int(GUILD))

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


"""
Whenever a message is sent
"""
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = message.content.lower()

    ambers_vocabulary = [
        'Miaoooo~',
        'Mao',
        'Meooow',
        'meow,.. meow,.. meow..'
    ]

    speak_commands = {"amber speak", "amber say something", "amber talk"}

    if text in speak_commands:
        response = random.choice(ambers_vocabulary)
        await message.channel.send(response)


"""
Whenever a new member joins the guild
"""
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel_send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


"""
Log all errors to a file instead
"""
@client.event
async def on_error(event, *args, **kwargs):
    e_info = sys.exc_info()
    with open('err.log', 'a') as f:
        f.write(f'{e_info}\n')
        print(f'**ERROR** {e_info[0]}: {e_info[1]}. Added a new entry to err.log')
    f.close()



client.run(TOKEN)