import os
import sys
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents,command_prefix='/')



"""
Whenever the connection is ready
"""
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, id=int(GUILD))

    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


"""
Whenever a message is sent
"""
@bot.event
async def on_message(message):
    if message.author == bot.user:
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
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel_send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

"""
Have Amber say something
"""

@bot.command(name='speak', help='Have Amber say something')
async def speak(ctx):
    ambers_vocabulary = [
        'Miaoooo~',
        'Mao',
        'Meooow',
        'meow,.. meow,.. meow..'
    ]

    response = random.choice(ambers_vocabulary)
    await ctx.send(response)


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


bot.run(TOKEN)