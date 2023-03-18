import os
import sys
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from lib import random_cfg_deriver

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents,command_prefix='!')

ambers_vocabulary = [
    'Miaoooo~',
    'Mao',
    'Meooow',
    'meow,.. meow,.. meow..'
]


"""
Whenever the connection is ready
"""
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, id=int(GUILD))
    response = random_cfg_deriver.process_grammar(f'lib/teatime.cfg')

    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
        f'Try this drink: {response}\n'
    )


"""
Whenever a message is sent
"""
@bot.listen('on_message')
async def on_amber_speak_message(message):
    if message.author == bot.user:
        return

    text = message.content.lower()

    speak_commands = {"amber speak", "amber say something", "amber talk"}

    if text in speak_commands:
        response = random.choice(ambers_vocabulary)
        await message.channel.send(response)


"""
Whenever a new member joins the server
"""
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel_send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


"""
Log all errors to a file instead
"""
@bot.event
async def on_error(event, *args, **kwargs):
    e_info = sys.exc_info()
    with open('err.log', 'a') as f:
        f.write(f'{e_info}\n')
        print(f'**ERROR** {e_info[0]}: {e_info[1]}. Added a new entry to err.log')
    f.close()


"""
Have Amber say something
"""
@bot.command(name='speak', help='Have Amber say something')
async def speak(ctx):
    response = random.choice(ambers_vocabulary)
    await ctx.send(response)


"""
Boba rec
"""
@bot.command(name='bobarec', help='Recommend a random boba drink')
async def bobarec(ctx):
    response = random_cfg_deriver.process_grammar('lib/teatime.cfg')
    await ctx.send(response)


bot.run(TOKEN)