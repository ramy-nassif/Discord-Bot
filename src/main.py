from os import getenv
import random
from time import sleep
from discord.ext import commands
import discord
from discord.utils import get
import requests

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=intents  # Set up basic permissions
)

bot.author_id = getenv('AUTHOR_ID')  # Change to your discord id


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


@bot.event
async def on_message(ctx):
    if ctx.content == 'Salut tout le monde':
        await ctx.reply('Salut tout seul')

    await bot.process_commands(ctx)


@bot.command()
async def pong(ctx):
    await ctx.send('pong')


@bot.command()
async def d6(ctx):
    await ctx.send(random.randint(1, 6))


@bot.command()
async def name(ctx):
    await ctx.send(ctx.author.name)


@bot.command()
async def admin(ctx, arg):
    if '#' not in arg:
        await ctx.send('Please use the format @username#0000')
        return

    member = get(ctx.guild.members, name=arg.split('#')[0], discriminator=arg.split('#')[1])

    if not member:
        await ctx.send('User not found')
        return

    if member.guild_permissions.administrator:
        await ctx.send(f'{arg} is already an admin')
        return

    role = get(ctx.message.guild.roles, name='Admin')
    if not role:
        role = await ctx.message.guild.create_role(name='Admin', permissions=discord.Permissions.all())

    await member.add_roles(role)
    await ctx.send(f'{arg} is now an admin')


@bot.command()
async def ban(ctx, arg):
    if '#' not in arg:
        await ctx.send('Please use the format @username#0000')
        return

    member = get(ctx.guild.members, name=arg.split('#')[0], discriminator=arg.split('#')[1])

    if not member:
        await ctx.send('User not found')
        return

    await member.ban()
    await ctx.send(f'{arg} has been banned')


@bot.command()
async def count(ctx):
    statuses = discord.Status
    for status in statuses:
        members = list(filter(lambda member: member.status == status, ctx.guild.members))
        await ctx.send(f'{status}: {len(members)}')
        if members:
            await ctx.send(', '.join([f'{member.name}#{member.discriminator}' for member in members]))


@bot.command()
async def xkcd(ctx):
    try:
        res = requests.get('https://c.xkcd.com/random/comic/')
        await ctx.send(res.url)
    except:
        await ctx.send('Failed to fetch a comic 😭')
        return


@bot.command()
async def poll(ctx, arg):
    if not arg:
        await ctx.send('Please provide a question')
        return

    await ctx.send('📊@here, this poll will expire in 10 seconds 😱')
    message = await ctx.send(f'{arg}')
    await message.add_reaction('👍')
    await message.add_reaction('👎')

    sleep(10)

    await ctx.send('Poll expired')
    await ctx.send(f'{arg}')
    message = await message.fetch()
    await ctx.send(f'👍: {len([reaction for reaction in message.reactions if reaction.emoji == "👍"]) - 1}')
    await ctx.send(f'👎: {len([reaction for reaction in message.reactions if reaction.emoji == "👎"]) - 1}')
    await message.delete()


token = getenv('BOT_TOKEN')
bot.run(token)  # Starts the bot
