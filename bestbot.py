########################################################################################################################
# INCLUDES
########################################################################################################################
import os
import sys
from datetime import date               # for blacklist
import string                           # for blacklist
from os import path                     # for find
import json                             # for conv
import random                           # for helix
from random import randint              # for roll
import urllib                           # for find
from requests import get                # for ip
from datetime import datetime, timezone # for timezone
from zoneinfo import ZoneInfo           # for timezone
import discord
from discord import app_commands

########################################################################################################################
# SETUP
########################################################################################################################
GH_LINK     = 'https://github.com/gentutu/bestbot'

colours = {
    'red'   : 0xAA2222,
    'green' : 0x22AA22,
    'blue'  : 0x224466,
    'grey'  : 0x666666
}

searchEngines = {
    'google' : 'https://www.google.com/search?q=',
    'yt'     : 'https://www.youtube.com/results?search_query=',
    'ddg'    : 'https://duckduckgo.com/?q=',
    'bing'   : 'https://www.bing.com/search?q=',
    'sp'     : 'https://startpage.com/do/search?q=',
    'wiki'   : 'https://en.wikipedia.org/wiki/Search?search=',
    'reddit' : 'https://www.reddit.com/search/?q=',
    'gh'     : 'https://github.com/search?q=',
    'aw'     : 'https://wiki.archlinux.org/index.php?search=',
    'gw'     : 'https://wiki.gentoo.org/index.php?search=',
    'pcgw'   : 'https://www.pcgamingwiki.com/w/index.php?search=',
    'wdb'    : 'https://www.winehq.org/search?q=',
    'pdb'    : 'https://www.protondb.com/search?q=',
    'ud'     : 'https://www.urbandictionary.com/define.php?term=',
    'mcw'    : 'https://minecraft.gamepedia.com/Special:Search?search=',
    'cheat'  : 'https://cheat.sh/'
}

files = {
    'f_blacklist'    : 'res/blacklist',
    'f_botToken'     : 'res/botToken',
    'f_channelEcho'  : 'res/channelEcho',
    'f_serverToken'  : 'res/serverToken',
    'f_cosmeticRoles': 'res/cosmeticRoles',
    'f_emoteHelix'   : 'res/emoteHelix',
    'f_currencyKey'  : 'res/currencyKey',
    'f_catKey'       : 'res/catKey',
    'f_helixReplies' : 'res/helixReplies'
}

if os.path.exists(files["f_blacklist"]):
    with open(files["f_blacklist"], 'r') as blacklistFile:
        global BLACKLIST
        BLACKLIST = blacklistFile.read().split()
        BLACKLIST = [element for element in BLACKLIST if element]
else:
    print(f'Error: {files["f_blacklist"]} file missing')
    sys.exit()

if os.path.exists(files["f_botToken"]):
    with open(files["f_botToken"], 'r') as botTokenFile:
        global BOT_TOKEN
        BOT_TOKEN = botTokenFile.read().strip('\n')
else:
    print(f'Error: {files["f_botToken"]} file missing')
    sys.exit()

if os.path.exists(files["f_serverToken"]):
    with open(files["f_serverToken"], 'r') as serverTokenFile:
        global SERVER_TOKEN
        SERVER_TOKEN = serverTokenFile.read().strip('\n')
        SERVER_TOKEN = discord.Object(id=int(SERVER_TOKEN))
else:
    print(f'Error: {files["f_serverToken"]} file missing')
    sys.exit()

if os.path.exists(files["f_channelEcho"]):
    with open(files["f_channelEcho"], 'r') as channelEchoFile:
        global CHANNEL_ECHO
        CHANNEL_ECHO = channelEchoFile.read().strip('\n')
else:
    print(f'Error: {files["f_channelEcho"]} file missing')
    sys.exit()

if os.path.exists(files["f_cosmeticRoles"]):
    with open(files["f_cosmeticRoles"], 'r') as cosmeticRolesFile:
        global COSMETIC_ROLES
        COSMETIC_ROLES = cosmeticRolesFile.read().split('\n')
        COSMETIC_ROLES = [element for element in COSMETIC_ROLES if element]
else:
    print(f'Error: {files["f_cosmeticRoles"]} file missing')
    sys.exit()

if os.path.exists(files["f_emoteHelix"]):
    with open(files["f_emoteHelix"], 'r') as emoteHelixFile:
        global EMOTE_HELIX
        EMOTE_HELIX = emoteHelixFile.read().strip('\n')
else:
    print(f'Error: {files["f_emoteHelix"]} file missing')
    sys.exit()

if os.path.exists(files["f_currencyKey"]):
    import currency
    with open(files["f_currencyKey"], 'r') as currencyKeyFile:
        global CURRENCY_KEY
        CURRENCY_KEY = currencyKeyFile.read().strip('\n') # https://www.currencyconverterapi.com/
else:
    CURRENCY_KEY = None

if os.path.exists(files["f_catKey"]):
    import cat
    with open(files["f_catKey"], 'r') as catKeyFile:
        global CAT_KEY
        CAT_KEY = catKeyFile.read().strip('\n') # https://thecatapi.com/ or https://thedogapi.com/
else:
    CAT_KEY = None

if os.path.exists(files["f_helixReplies"]):
    with open(files["f_helixReplies"], 'r') as helixRepliesFile:
        global HELIX_REPLIES
        HELIX_REPLIES = open(files["f_helixReplies"], 'r').read().split('\n')
        HELIX_REPLIES = [element for element in HELIX_REPLIES if element]
else:
    print(f'Error: {files["f_helixReplies"]} file missing')
    sys.exit()

class bestbot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild = SERVER_TOKEN)
        await self.tree.sync(guild = SERVER_TOKEN)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
client = bestbot(intents=intents)

@client.event
async def on_ready():
    print('Bestbot online.')
    await client.change_presence(status = discord.Status.online)

########################################################################################################################
# LOCAL API
########################################################################################################################
async def echoMessage(reason, message, colour):
    echoChannel = client.get_channel(int(CHANNEL_ECHO))

    if message.author.id == client.user.id:
        return

    if message.attachments:
        image = message.attachments[0]
        client.echoLog[message.guild.id] = (image.proxy_url, message.content, message.author,
                                            message.channel.name, message.created_at)
    else:
        client.echoLog[message.guild.id] = (message.content,message.author, message.channel.name,
                                            message.created_at)

    try:
        image_proxy_url, contents,author, channel_name, time = client.echoLog[message.guild.id]
    except:
        contents,author, channel_name, time = client.echoLog[message.guild.id]

    try:
        embed = discord.Embed(description = contents,
                              color       = colour,
                              timestamp   = time)
        #embed.set_image(url = image_proxy_url)
        embed.set_author(name     = f"{message.author.name}#{message.author.discriminator}",
                         icon_url = message.author.avatar)
        embed.set_footer(text = f"{reason} in #{channel_name}")
        await echoChannel.send(embed = embed)
    except:
        embed = discord.Embed(description = contents,
                              color       = colour,
                              timestamp   = time)
        embed.set_author(name     = f"{message.author.name}#{message.author.discriminator}",
                         icon_url = message.author.avatar)
        embed.set_footer(text = f"{reason} in #{channel_name}")
        await echoChannel.send(embed = embed)

    async for entry in message.guild.audit_logs(action = discord.AuditLogAction.message_delete):
        action = discord.AuditLogAction.message_delete

########################################################################################################################
# MODERATION
########################################################################################################################
@client.tree.command(description = "Show the host\'s WAN IP.") ###################################################### ip
@app_commands.checks.has_role("admin")
async def ip(context: discord.Interaction):
    host_wan_ip = get('https://api.ipify.org').text
    embed = discord.Embed(title       = "Host WAN IP",
                          description = f'||`{host_wan_ip}`||',
                          color       = colours["red"])
    await context.response.send_message(embed = embed, ephemeral = True)

@client.tree.command(description = "Remove the most recent messages.") ########################################### clear
@app_commands.checks.has_any_role("admin", "mod")
@app_commands.describe(amount = "Number of message to delete")
async def clear(context: discord.Interaction, amount: app_commands.Range[int, 1, None]):
    await context.response.send_message("Removed the most recent messages.", ephemeral = True)
    await context.channel.purge(limit = amount)

@client.tree.command(description = "Set a channel's slow mode") ################################################### slow
@app_commands.describe(interval = "Delay between messages", reason = "Reason for slowdown")
@app_commands.checks.has_any_role("admin", "mod")
async def slow(context: discord.Interaction, interval: app_commands.Range[str, 2, 3], reason: str):
    duration = {'off': 0,   '5s' : 5,   '10s': 10,  '15s': 15,   '30s': 30,   '1m' : 60,   '2m' : 120,
                '5m' : 300, '10m': 600, '15m': 900, '30m': 1800, '1h' : 3600, '2h' : 7200, '6h' : 21600}

    if interval in duration:
        await context.channel.edit(reason = f'{reason}', slowmode_delay = int(duration[interval]))
        await context.response.send_message(f'Set slow mode to `{interval}` with reason `{reason}`.')
    else:
        await context.response.send_message("Unknown slow interval", ephemeral = True)

@client.tree.command(description = "Update a channel's topic.") ################################################## topic
@app_commands.describe(request = "New channel topic")
@app_commands.checks.has_any_role("admin", "mod")
async def newtopic(context: discord.Interaction, request: app_commands.Range[str, 1, 64]):
    await context.channel.edit(topic = request)
    await context.response.send_message(f'Channel topic updated to `{request}`.')

########################################################################################################################
# UTILITIES
########################################################################################################################
@client.tree.command(description = "Link towards the bot\'s source code.") ###################################### source
async def source(context: discord.Interaction):
    embed = discord.Embed(title       = "Best Source",
                          description = f"<{GH_LINK}>",
                          color       = colours["grey"])
    await context.response.send_message(embed = embed, ephemeral = True)

@client.tree.command(description = "Check  network quality.") ##################################################### ping
async def ping(context: discord.Interaction):
    await context.response.send_message(f'pong! `{round(client.latency * 1000)}ms`', ephemeral = True)

@client.tree.command(description = "Roll for a random number up to a maximum.") ################################### roll
@app_commands.describe(max = "Max possible roll", terms = "Terms of the roll")
async def roll(context: discord.Interaction, max:  app_commands.Range[int, 1, None], terms: str):
    await context.response.send_message(f'Rolled **{randint(0, max)}** for *{terms}*.')

@client.tree.command(description = "Toss a coin.") ################################################################ coin
@app_commands.describe(terms = "Terms of the flip")
async def coin(context: discord.Interaction, terms: str):
    sides = ['heads', 'tails']
    if terms is None:
        await context.response.send_message(f'Tossed **{random.choice(sides)}**.')
    else:
        await context.response.send_message(f'Tossed **{random.choice(sides)}** for *{terms}*.')

@client.tree.command(description = "Consult the Helix Fossil.") ################################################## helix
@app_commands.describe(question = "It shall answer")
async def helix(context: discord.Interaction, question: str):
    await context.response.send_message(f'{question}\n{EMOTE_HELIX} *{random.choice(HELIX_REPLIES)}* {EMOTE_HELIX}')

@client.tree.command(description = "Search the web.") ############################################################# find
@app_commands.describe(engine = "Search engine", query = "Search query")
async def find(context: discord.Interaction, engine: str, query: str):
    engine = engine.lower()

    if engine not in searchEngines: # check if the requested engine exists
        await context.response.send_message(f'Searching for *{query}*\nUnknown search engine.', ephemeral = True)
    else:
        search_input = searchEngines[engine] + urllib.parse.quote(query)
        await context.response.send_message(f'{engine.capitalize()} search: *{query}*\nYour results: <{search_input}>')

@client.tree.command(description = "Toggle a role.") ############################################################## role
@app_commands.describe(request = "Role to toggle")
async def role(context: discord.Interaction, request: str):
    if request == 'list':
        await context.response.send_message(f'Available roles: `{"`, `".join(COSMETIC_ROLES)}`.', ephemeral = True)
        return

    if request in COSMETIC_ROLES:
        request = discord.utils.get(context.guild.roles, name = request)
        if request in context.user.roles:
            await discord.Member.remove_roles(context.user, request)
            await context.response.send_message(f'Removed `{request}` role.', ephemeral = True)
        else:
            await discord.Member.add_roles(context.user, request)
            await context.response.send_message(f'Added `{request}` role.', ephemeral = True)
    else:
        await context.response.send_message("Unsupported role.", ephemeral = True)

@client.tree.command(description = "Convert currency. Use the 3-letter currency codes.") ########################## conv
@app_commands.describe(amount = "Amount to convert", source = "Source currency", target = "Target currency")
async def conv(context: discord.Interaction, amount: app_commands.Range[int, 1, None],
                                             source: app_commands.Range[str, 3, 3],
                                             target: app_commands.Range[str, 3, 3]):
    source = source.upper()
    target = target.upper()

    if not 'currencies.json' in os.listdir('./res'):
        await currency.retrieve_currencies(CURRENCY_KEY)

    with open('./res/currencies.json', 'r') as stored_curr:
        available_curr = json.load(stored_curr)

    if source not in available_curr or \
       target not in available_curr:
        await context.response.send_message("Unknown currency code.", ephemeral = True)
        return

    if source == target:
        await context.response.send_message("Nothing to convert.", ephemeral = True)
        return

    exchanged = await currency.currency_convert(CURRENCY_KEY, amount, source, target)
    await context.response.send_message(f'{amount:.2f} `{source}` ≈ `{target}` {exchanged:.2f}')

@client.tree.command(description = "Request a random animal picture.") ############################################# pls
@app_commands.describe(animal = "\"cat\" or \"dog\"")
async def pls(context: discord.Interaction, animal: app_commands.Range[str, 3, 3]):
    supported_animals = ['cat', 'dog']

    if(animal in supported_animals):
        URL = await cat.get(animal, CAT_KEY, random.choice(['jpg', 'gif']))
        await context.response.send_message(f'{URL}')
    else:
        await context.response.send_message("Unknown request", ephemeral = True)

@client.tree.command(description = "Show the time of a place.") ############################################### timezone
@app_commands.describe(place = "TZ time zone")
async def timezone(context: discord.Interaction, place: str):
    place = place.title()

    try:
        time = datetime.now(ZoneInfo(str(place)))
    except:
        tzLink = 'https://en.wikipedia.org/wiki/List_of_tz_database_time_zones'
        await context.response.send_message(f'Incorrect timezone; see <{tzLink}>.', ephemeral = True)
        return

    time = discord.utils.format_dt(time, 't')
    await context.response.send_message(f'It\'s {time} in {place}.')

@client.tree.command(description = "Show the system uptime.") ################################################### uptime
@app_commands.checks.has_any_role("admin", "mod")
async def uptime(context: discord.Interaction):
    with open('/proc/uptime', 'r') as uptimeFile:
        time = float(uptimeFile.readline().split()[0])

    days  = time / 86400
    hours = time / 3600 % 24

    await context.response.send_message(f'Approximate uptime: `{int(days)}d {int(hours)}h`', ephemeral = True)

@client.tree.command(description = "Show the server join date.") ################################################ uptime
async def joined(context: discord.Interaction):
    embed = discord.Embed(title       = "Your join date",
                          description = f"{discord.utils.format_dt(context.user.joined_at, 'D')}",
                          color       = colours["grey"])
    await context.response.send_message(embed = embed, ephemeral = True)

########################################################################################################################
# EVENTS
########################################################################################################################
@client.event ################################################################################################ blacklist
async def on_message(message):
    allowed = True
    current_message = message.content.lower()
    dad_check       = current_message
    current_message = current_message.replace(" ", "")

    if date.today().weekday() != 2 and ":wednesday:" in current_message:
        await message.delete()
        allowed = False
    else:
        for word in BLACKLIST:
            if word in current_message.replace(" ", ""):
                await message.delete()
                allowed = False

    if allowed:
        if random.random() < 0.05:
            dad_check = dad_check.replace('\'', '')
            if dad_check.startswith('im '):
                name = message.content.split()
                name = ' '.join(name[1:])
                await message.channel.send(f'hello {name} im dad')
            elif dad_check.startswith('i am '):
                name = message.content.split()
                name = ' '.join(name[2:])
                await message.channel.send(f'hello {name} im dad')

@client.event ################################################################################################ blacklist
async def on_message_edit(before, after):
    if before.content == after.content:
        return

    await echoMessage("Edited from", before, colours["green"])
    await echoMessage("Edited to"  , after,  colours["blue"])

    current_message = after.content.lower()
    if date.today().weekday() != 2 and ":wednesday:" in current_message:
        await after.delete()
    else:
        for word in BLACKLIST:
            if word in current_message.replace(" ", ""):
                await after.delete()

@client.event ############################################################################################# deleted echo
async def on_message_delete(message):
    await echoMessage("Deleted", message, colours["red"])

########################################################################################################################
# RUN
########################################################################################################################
client.run(BOT_TOKEN)

########################################################################################################################
# END OF FILE
########################################################################################################################
