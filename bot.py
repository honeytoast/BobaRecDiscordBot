import os
import re
import sys
import random
import discord
import json
from dotenv import load_dotenv
from discord.ext import commands
from lib import random_cfg_deriver
from lib import lastepoch_helper

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

"""
[Last Epoch] Show leaderboard for death counters
"""
@bot.command(name='deaths', help='Show the current leaderboard for Last Epoch (hardcore mode) deaths')
async def deaths(ctx):
    response = """```\n
*-------------------------------*
|    Death Count Leaderboard    |
*-------------------------------*

"""
    with open('lib/lastepoch_deathcounts.json', 'r') as f:
        death_counts = json.load(f, parse_int=lambda x: int(x))
    f.close()

    sorted_counts = sorted(death_counts.items(), key=lambda kv: (kv[1][1], kv[0]), reverse=True)
    for count in sorted_counts:
        response += f'{count[1][0]}: {count[1][1]}\n'
        if len(count[1]) == 3:
            # list the primary causes of death
            for val in count[1][2].items():
                try:
                    causer = await ctx.guild.fetch_member(int(val[0]))
                    response += f'\t{val[1]} associated with {causer.display_name}\n'
                except Exception:
                    pass
    response += "\n```"
    await ctx.send(response)

"""
[Last Epoch] Increment death count
"""
@bot.command(name='idied', help="Add 1 to your LE death count (optional: @ a user to associate cause of death)")
async def idied(ctx, *args):
    with open('lib/lastepoch_deathcounts.json', 'r') as f:
        death_counts = json.load(f, parse_int=lambda x: int(x))
    f.close()

    mykey = str(ctx.message.author.id)

    # we'll always use the display name so it updates if they've updated it
    myname = ctx.message.author.display_name

    causer_id = None

    # keep tally on members causing other members' deaths
    if len(args) == 0:
        print("no args\n")
    else:
        print(args)
        arg1 = re.match('<@([0-9]+)>', args[0])
        if arg1 != None:
            causer_id = arg1.groups()[0]

    causer = None

    if causer_id != None:
        causer = await ctx.guild.fetch_member(int(causer_id))

    if mykey in death_counts:
        death_counts[mykey][0] = myname
        death_counts[mykey][1] += 1
        if len(death_counts[mykey]) == 3 and causer != None:
            if causer_id in death_counts[mykey][2]:
                death_counts[mykey][2][causer_id] += 1
            else:
                death_counts[mykey][2][causer_id] = 1
        elif len(death_counts[mykey]) < 3:
            # retrofit older entries
            death_counts[mykey].append(dict())
            if causer_id != None:
                death_counts[mykey][2][causer_id] = 1
    else:
        # net new entries
        if causer == None:
            death_counts[mykey] = [myname, 1, dict()]
        else:
            death_counts[mykey] = [myname, 1, {causer_id: 1}]

    with open('lib/lastepoch_deathcounts.json', 'w') as f:
        json.dump(death_counts, f, indent=4)
    f.close()

    # response = random.choice(lastepoch_helper.rip_messages)
    response = "Oof! I incremented your death count by 1, you can thank me with some treats :3\n"
    response += f'```\n{death_counts[mykey][0]}: {death_counts[mykey][1]}\n```'
    if causer_id != None:
        response += f'Associated this death with {causer.display_name}\n'

    await ctx.send(response)

bot.run(TOKEN)