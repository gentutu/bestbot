########################################################################################################################
# INCLUDES
########################################################################################################################
import discord
from discord.ext import commands
import random # for helix
from random import randint # for roll
from requests import get # for ip
import urllib # for find
from urllib import request # for find

########################################################################################################################
# SETUP
########################################################################################################################
client = commands.Bot(command_prefix = '/')

ghlink = 'https://github.com/gentutu/bestbot'

btoken = open('res/btoken', 'r').read().strip('\n')
cadmin = open('res/cadmin', 'r').read().strip('\n')
ehelix = open('res/ehelix', 'r').read().strip('\n')

@client.event
async def on_ready():
    print('Bestbot online.')
    await client.change_presence(status = discord.Status.online, activity = discord.Game('with admin powers'))

########################################################################################################################
# MODERATION
########################################################################################################################
@client.command(brief       = 'Shows the host\'s WAN IP', ########################################################### ip
                description = '[admin] Shows the host\'s WAN IP.')
async def ip(context, noarg = None):
    if(True == context.author.guild_permissions.administrator): # check for user permissions
        if(None == noarg): # check for no arguments
            if(int(cadmin) == context.channel.id):
                ip = get('https://api.ipify.org').text
                await context.send(f'{context.author.mention} WAN IP: ||`{ip}`||')
            else:
                await context.send(f'{context.author.mention} Command not available on current channel.')
        else:
            await context.send(f'{context.author.mention} Command does not take arguments.')
    else:
        await context.send(f'{context.author.mention} Permission denied.')

@client.command(brief       = 'Deletes a specified amount of messages', ########################################## clear
                description = '[admin/mod] Deletes a specified amount of messages. Call with \'confirm\' argument.')
async def clear(context, amount = None, confirm = None, noarg = None):
    if(True == context.author.guild_permissions.manage_messages): # check for user permissions
        try: # check for correct argument type
            if((None == noarg) and ('confirm' == confirm)): # check for no third argument
                isinstance(amount, int) # try to raise exception if wrong argument
                amount = int(amount)
                if(0 == amount):
                    raise Exception()
                elif(1 == amount):
                    await context.channel.purge(limit = amount + 1)
                    await context.send(f'{context.author.mention} cleared the last message.')
                else:
                    await context.channel.purge(limit = amount + 1)
                    await context.send(f'{context.author.mention} cleared the last {amount} messages.')
            else:
                raise Exception()
        except Exception:
            await context.send(f'{context.author.mention} Incorrect arguments. Use `!clear [amount > 0] confirm`.')
    else:
        await context.send(f'{context.author.mention} Permission denied.')

########################################################################################################################
# UTILITIES
########################################################################################################################
@client.command(brief       = 'Links towards the bot\'s source code', ########################################### source
                description = 'Links towards the bot\'s source code.')
async def source(context, noarg = None):
    if(None == noarg): # check for no arguments
        await context.send(f'{context.author.mention} See this for my source code: <{ghlink}>')
    else:
        await context.send(f'{context.author.mention} Command does not take arguments.')

@client.command(brief       = 'Checks bot status and network quality', ############################################ ping
                description = 'Check  bot status and network quality.')
async def ping(context, noarg = None):
    if(None == noarg): # check for no arguments
        await context.send(f'{context.author.mention} pong! `{round(client.latency * 1000)}ms`')
    else:
        await context.send(f'{context.author.mention} Command does not take arguments.')

@client.command(brief       = 'Rolls for a random number up to a maximum', ######################################## roll
                description = 'Rolls for a random number up to a maximum.',
                aliases     = ['dice'])
async def roll(context, maximum = None, *, terms = None):
    try: # check for correct argument type
        isinstance(maximum, int)
        maximum = int(maximum)
        if(1 < maximum):
            if(None == terms):
                await context.send(f'{context.author.mention} rolled {randint(1, maximum)}.')
            else:
                await context.send(f'{context.author.mention} rolled {randint(1, maximum)} for *{terms}*.')
        else:
            raise Exception()
    except Exception:
        await context.send(f'{context.author.mention} Incorrect arguments. Use `!roll [maximum > 1]`.')

@client.command(brief       = 'Tosses a coin', #################################################################### coin
                description = 'Tosses a coin. Accepts terms freely.',
                aliases     = ['toss'])
async def coin(context, *, terms = None):
    sides = ['heads', 'tails']
    if(None == terms):
        await context.send(f'{context.author.mention} tossed **{random.choice(sides)}**.')
    else:
        await context.send(f'{context.author.mention} tossed **{random.choice(sides)}** for *{terms}*.')

@client.command(brief       = 'Consult the Helix Fossil', ######################################################## helix
                description = 'Consult the Helix Fossil. It shall answer.',
                aliases = ['fossil'])
async def helix(context, *, question = None):
    responses = ['It is certain.'          , 'It is decidedly so.', 'Without a doubt.'          , 'Yes – definitely.'  ,
                 'You may rely on it.'     , 'As I see it, yes.'  , 'Most likely.'              , 'Outlook good.'      ,
                 'Yes.'                    , 'Signs point to yes.', 'Reply hazy, try again.'    , 'Ask again later.'   ,
                 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', 'Don\'t count on it.',
                 'My reply is no.'         ,  'My sources say no.', 'Outlook not so good.'      , 'Very doubtful.'     ,
                 'Wouldn\'t you want to know, weather boy?']
    if(None != question): # check for at least 1 argument
        await context.send(f'{context.author.mention} Helix Fossil says: {ehelix} *{random.choice(responses)}* {ehelix}')
    else:
        await context.send(f'{context.author.mention} Consult the Fossil. {ehelix}')

@client.command(brief       = 'Performs a web search', ############################################################ find
                description = 'Search a lot of places. Too many to list here. See the source code.')
async def find(context, engine = None, *, query = None):
    if(   'google'     == engine):                        header = 'https://google.com/search?q='
    elif(('youtube'    == engine) or ('yt'   == engine)): header = 'https://www.youtube.com/results?search_query='
    elif(('duckduckgo' == engine) or ('ddg'  == engine)): header = 'https://duckduckgo.com/?q='
    elif( 'bing'       == engine):                        header = 'https://bing.com/search?q='
    elif(('wikipedia'  == engine) or ('wiki' == engine)): header = 'https://en.wikipedia.org/wiki/Search?search='
    elif(('github'     == engine) or ('gh'   == engine)): header = 'https://github.com/search?q='
    elif(('archwiki'   == engine) or ('aw'   == engine)): header = 'https://wiki.archlinux.org/index.php?search='
    elif(('gentoowiki' == engine) or ('gw'   == engine)): header = 'https://wiki.gentoo.org/index.php?&search='
    elif(('winedb'     == engine) or ('wdb'  == engine)): header = 'https://www.winehq.org/search?q='
    elif(('protondb'   == engine) or ('pdb'  == engine)): header = 'https://www.protondb.com/search?q='
    elif(('pornhub'    == engine) or ('ph'   == engine)):
        await context.send(f'{context.author.mention} No.')
        return
    else:
        await context.send(f'{context.author.mention} Unknown search engine.')
        return
    if(None != query): # check for at least 1 search term
        searchInput = header + urllib.parse.quote(query)
        await context.send(f'{context.author.mention} Your search results: <{searchInput}>')
    else:
        await context.send(f'{context.author.mention} What should I search for?')

########################################################################################################################
# RUN
########################################################################################################################
client.run(btoken)
