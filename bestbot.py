########################################################################################################################
# INCLUDES
########################################################################################################################
import os
import json                # for conv
import discord
from discord.ext import commands
import random              # for helix
from random import randint # for roll
from requests import get   # for ip
import urllib              # for find
from urllib import request # for find

########################################################################################################################
# SETUP
########################################################################################################################
client = commands.Bot(command_prefix = '/')

ghlink     = 'https://github.com/gentutu/bestbot'
errorReply = 'Incorrect command usage; see `/help [command]`'

colours = {
    'red'   : 0xAA2222,
    'green' : 0x22AA22,
    'blue'  : 0x224466
}

files = {
    'f_blacklist'    : 'res/blacklist',
    'f_botToken'     : 'res/botToken',
    'f_channelAdmin' : 'res/channelAdmin',
    'f_cosmeticRoles': 'res/cosmeticRoles',
    'f_emoteHelix'   : 'res/emoteHelix',
    'f_currencyCache': 'res/currencyCache',
    'f_helixReplies' : 'res/helixReplies'
}

if os.path.exists(files["f_blacklist"]):
    with open(files["f_blacklist"], 'r') as blacklistFile:
        global blacklist
        blacklist = blacklistFile.read().split()
        blacklist = [element for element in blacklist if element]
else:
    print(f'Error: {files["f_blacklist"]} file missing')
    exit()

if os.path.exists(files["f_botToken"]):
    with open(files["f_botToken"], 'r') as botTokenFile:
        global botToken
        botToken = botTokenFile.read().strip('\n')
else:
    print(f'Error: {files["f_botToken"]} file missing')
    exit()

if os.path.exists(files["f_channelAdmin"]):
    with open(files["f_channelAdmin"], 'r') as channelAdminFile:
        global channelAdmin
        channelAdmin = channelAdminFile.read().strip('\n')
else:
    print(f'Error: {files["f_channelAdmin"]} file missing')
    exit()

if os.path.exists(files["f_cosmeticRoles"]):
    with open(files["f_cosmeticRoles"], 'r') as cosmeticRolesFile:
        global cosmeticRoles
        cosmeticRoles = cosmeticRolesFile.read().split('\n')
        cosmeticRoles = [element for element in cosmeticRoles if element]
else:
    print(f'Error: {files["f_cosmeticRoles"]} file missing')
    exit()

if os.path.exists(files["f_emoteHelix"]):
    with open(files["f_emoteHelix"], 'r') as emoteHelixFile:
        global emoteHelix
        emoteHelix = emoteHelixFile.read().strip('\n')
else:
    print(f'Error: {files["f_emoteHelix"]} file missing')
    exit()

if os.path.exists(files["f_currencyCache"]):
    import currency
    with open(files["f_currencyCache"], 'r') as currencyCacheFile:
        global currencyCache
        currencyCache = currencyCacheFile.read().strip('\n') # https://www.currencyconverterapi.com/
else:
    currencyCache = None

if os.path.exists(files["f_helixReplies"]):
    with open(files["f_helixReplies"], 'r') as helixRepliesFile:
        global helixReplies
        helixReplies = open(files["f_helixReplies"], 'r').read().split('\n')
        helixReplies = [element for element in helixReplies if element]
else:
    print(f'Error: {files["f_helixReplies"]} file missing')
    exit()

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
    if(True != context.author.guild_permissions.administrator): # check for user permissions
        await context.send(f'{context.author.mention} Permission denied.')
        return

    if(None != noarg): # check for no arguments
        await context.send(f'{context.author.mention} {errorReply}.')
        return

    if(int(channelAdmin) == context.channel.id):
        ip = get('https://api.ipify.org').text
        embed = discord.Embed(title = "Host WAN IP", description = f'||`{ip}`||', color = colours["red"])
        await context.send(embed = embed)
    else:
        await context.send(f'{context.author.mention} Command not available on current channel.')

@client.command(brief       = 'Deletes a specified amount of messages', ########################################## clear
                description = '[admin/mod] Deletes a specified amount of messages. Call with \'confirm\' argument.')
async def clear(context, amount = None, confirm = None, noarg = None):
    if(True != context.author.guild_permissions.manage_messages): # check for user permissions
        await context.send(f'{context.author.mention} Permission denied.')
        return

    try: # check for correct argument type
        if((None == noarg) and ('confirm' == confirm)): # check for no third argument
            amount = int(amount)
            if(1 > amount):
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
        await context.send(f'{context.author.mention} {errorReply}.')

########################################################################################################################
# UTILITIES
########################################################################################################################
@client.command(brief       = 'Links towards the bot\'s source code', ########################################### source
                description = 'Links towards the bot\'s source code.')
async def source(context, noarg = None):
    if(None == noarg): # check for no arguments
        embed = discord.Embed(title = "Best Source", description = f"<{ghlink}>", color = colours["red"])
        await context.send(embed = embed)
    else:
        await context.send(f'{context.author.mention} {errorReply}.')

@client.command(brief       = 'Checks bot status and network quality', ############################################ ping
                description = 'Check  bot status and network quality.',
                aliases     = ['pong'])
async def ping(context, noarg = None):
    if(None == noarg): # check for no arguments
        if('pong' == context.invoked_with):
            await context.send(f':dagger:')
        else:
            await context.send(f'pong! `{round(client.latency * 1000)}ms`')
    else:
        await context.send(f'{context.author.mention} {errorReply}.')

@client.command(brief       = 'Rolls for a random number up to a maximum', ######################################## roll
                description = 'Rolls for a random number up to a maximum.')
async def roll(context, maximum = None, *, terms = None):
    try: # check for correct argument type
        maximum = int(maximum)
        if(1 < maximum):
            if(None == terms):
                await context.send(f'{context.author.mention} rolled {randint(1, maximum)}.')
            else:
                await context.send(f'{context.author.mention} rolled {randint(1, maximum)} for *{terms}*.')
        else:
            raise Exception()
    except Exception:
        await context.send(f'{context.author.mention} {errorReply}`.')

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
                description = 'Consult the Helix Fossil. It shall answer.')
async def helix(context, *, question = None):
    if(None != question): # check for at least 1 argument
        await context.send(f'{context.author.mention} Helix Fossil says: {emoteHelix} *{random.choice(helixReplies)}* {emoteHelix}')
    else:
        await context.send(f'{context.author.mention} Consult the Fossil. {emoteHelix}')

@client.command(brief       = 'Performs a web search', ############################################################ find
                description = 'Search a lot of places. Too many to list here. See the source code.')
async def find(context, engine = None, *, query = None):
    if(  'google' == engine): header = 'https://www.google.com/search?q='
    elif('yt'     == engine): header = 'https://www.youtube.com/results?search_query='
    elif('ddg'    == engine): header = 'https://duckduckgo.com/?q='
    elif('bing'   == engine): header = 'https://www.bing.com/search?q='
    elif('sp'     == engine): header = 'https://startpage.com/do/search?q='
    elif('wiki'   == engine): header = 'https://en.wikipedia.org/wiki/Search?search='
    elif('reddit' == engine): header = 'https://www.reddit.com/search/?q='
    elif('gh'     == engine): header = 'https://github.com/search?q='
    elif('aw'     == engine): header = 'https://wiki.archlinux.org/index.php?search='
    elif('gw'     == engine): header = 'https://wiki.gentoo.org/index.php?search='
    elif('pcgw'   == engine): header = 'https://www.pcgamingwiki.com/w/index.php?search='
    elif('wdb'    == engine): header = 'https://www.winehq.org/search?q='
    elif('pdb'    == engine): header = 'https://www.protondb.com/search?q='
    elif('ud'     == engine): header = 'https://www.urbandictionary.com/define.php?term='
    elif('mcw'    == engine): header = 'https://minecraft.gamepedia.com/Special:Search?search='
    elif('ph'     == engine):
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

@client.command(brief       = 'Toggles a role', ################################################################### role
                description = 'Toggles a role. List all options with the `list` argument.')
async def role(context, role = None, noarg = None):
    member = context.author
    if(None != noarg):
        await context.send(f'{context.author.mention} {errorReply}.')
        return

    if('list' == role):
        await context.send(f'{context.author.mention} Available roles: {cosmeticRoles}.')
        return

    if(role in cosmeticRoles):
        role = discord.utils.get(member.guild.roles, name = role)
        if(role in member.roles):
            await discord.Member.remove_roles(member, role)
            await context.send(f'{context.author.mention} Removed role.')
        else:
            await discord.Member.add_roles(member, role)
            await context.send(f'{context.author.mention} Added role.')
    elif(None == role):
        await context.send(f'{context.author.mention} {errorReply}.')
    else:
        await context.send(f'{context.author.mention} Unsupported role.')


@client.command(brief       = 'Converts currency', ################################################################ conv
                description = 'Converts currency. Use the 3-letter currency codes.')
async def conv(context, amount = None, source = None, target = None, noarg = None):
    try: # check for int amount
        amount = float(amount)
        if((None != noarg)  or \
           (None == source) or \
           (None == target) or \
           (None == amount)):
            raise Exception()
    except Exception:
        await context.send(f'{context.author.mention} {errorReply}.')
        return

    source = source.upper()
    target = target.upper()

    if not 'currencies.json' in os.listdir('./res'): # retrieve currency data if we don't have it stored.
        await currency.retrieve_currencies(currencyCache)

    with open('./res/currencies.json', 'r') as storedCurr: # load list of currencies
        availableCurr = json.load(storedCurr)

    if(source not in availableCurr) or \
      (target not in availableCurr):
        await context.send(f'{context.author.mention} Unknown currency code.')
        return

    if(source == target):
        await context.send(f'{context.author.mention} Nothing to convert.')
        return

    exchanged = await currency.currency_convert(currencyCache, amount, source, target)
    await context.send(f'{context.author.mention} {amount:.2f} `{source}` ≈ `{target}` {exchanged:.2f}')


########################################################################################################################
# EVENTS
########################################################################################################################
@client.event ################################################################################################ blacklist
async def on_message(message):
    for word in blacklist:
        currentMessage = message.content.lower()
        if word in currentMessage.replace(" ", ""):
            await message.delete()
    await client.process_commands(message)

########################################################################################################################
# RUN
########################################################################################################################
client.run(botToken)

########################################################################################################################
# END OF FILE
########################################################################################################################
