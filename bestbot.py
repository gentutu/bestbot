########################################################################################################################
# INCLUDES
########################################################################################################################
import os
from   os import path
import sys
import string
from typing import Literal
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo
import discord
from   discord import app_commands
import json
import random
from   random import randint
import urllib
from requests import get

########################################################################################################################
# CFG
########################################################################################################################
GH_LINK = '<https://github.com/gentutu/bestbot>'

colours = {
    'red'  : 0xAA2222,
    'green': 0x22AA22,
    'blue' : 0x224466,
    'grey' : 0x666666
}

slowIntervals = {'off': 0,   '5s' : 5,   '10s': 10,  '15s': 15,   '30s': 30,   '1m' : 60,   '2m' : 120,
                 '5m' : 300, '10m': 600, '15m': 900, '30m': 1800, '1h' : 3600, '2h' : 7200, '6h' : 21600}
SLOWMODE_LIST = Literal[tuple(list(slowIntervals))]

files = {
    'f_blacklist'    : 'res/blacklist',
    'f_botToken'     : 'res/botToken',
    'f_catKey'       : 'res/catKey',
    'f_channelEcho'  : 'res/channelEcho',
    'f_cosmeticRoles': 'res/cosmeticRoles',
    'f_currencyKey'  : 'res/currencyKey',
    'f_currencyList' : 'res/currencyList',
    'f_helixEmote'   : 'res/helixEmote',
    'f_helixReplies' : 'res/helixReplies',
    'f_searchEngines': 'res/searchEngines',
    'f_serverToken'  : 'res/serverToken',
}

########################################################################################################################
# SETUP
########################################################################################################################
if os.path.exists(files["f_blacklist"]): ##################################################################### blacklist
    with open(files["f_blacklist"], 'r') as blacklistFile:
        global BLACKLIST
        BLACKLIST = blacklistFile.read().split()
        BLACKLIST = [element for element in BLACKLIST if element]
else:
    print(f'Error: {files["f_blacklist"]} file missing')
    sys.exit()

if os.path.exists(files["f_botToken"]): ####################################################################### botToken
    with open(files["f_botToken"], 'r') as botTokenFile:
        global BOT_TOKEN
        BOT_TOKEN = botTokenFile.read().strip('\n')
else:
    print(f'Error: {files["f_botToken"]} file missing')
    sys.exit()

if os.path.exists(files["f_catKey"]): ########################################################################### catKey
    import cat
    with open(files["f_catKey"], 'r') as catKeyFile:
        global CAT_KEY
        CAT_KEY = catKeyFile.read().strip('\n') # https://thecatapi.com/ or https://thedogapi.com/
else:
    CAT_KEY = None

if os.path.exists(files["f_channelEcho"]): ################################################################# channelEcho
    with open(files["f_channelEcho"], 'r') as channelEchoFile:
        global CHANNEL_ECHO
        CHANNEL_ECHO = channelEchoFile.read().strip('\n')
else:
    print(f'Error: {files["f_channelEcho"]} file missing')
    sys.exit()

if os.path.exists(files["f_cosmeticRoles"]): ############################################################# cosmeticRoles
    with open(files["f_cosmeticRoles"], 'r') as cosmeticRolesFile:
        global COSMETIC_ROLES
        COSMETIC_ROLES = cosmeticRolesFile.read().split('\n')
        COSMETIC_ROLES = [element for element in COSMETIC_ROLES if element]
        COSMETIC_ROLES = Literal[tuple(COSMETIC_ROLES)]
else:
    print(f'Error: {files["f_cosmeticRoles"]} file missing')
    sys.exit()

if os.path.exists(files["f_currencyKey"]): ################################################################# currencyKey
    import currency
    with open(files["f_currencyKey"], 'r') as currencyKeyFile:
        global CURRENCY_KEY
        CURRENCY_KEY = currencyKeyFile.read().strip('\n') # https://www.currencyconverterapi.com/
else:
    CURRENCY_KEY = None

if os.path.exists(files["f_currencyList"]): ############################################################### currencyList
    import currency
    with open(files["f_currencyList"], 'r') as currencyListFile:
        global CURRENCY_LIST
        CURRENCY_LIST = currencyListFile.read().split('\n') # https://www.currencyconverterapi.com/
        CURRENCY_LIST = [element for element in CURRENCY_LIST if element]
        CURRENCY_LIST = Literal[tuple(CURRENCY_LIST)]
else:
    print(f'Error: {files["f_currencyList"]} file missing')
    sys.exit()

if os.path.exists(files["f_helixEmote"]): ################################################################### helixEmote
    with open(files["f_helixEmote"], 'r') as helixEmoteFile:
        global HELIX_EMOTE
        HELIX_EMOTE = helixEmoteFile.read().strip('\n')
else:
    print(f'Error: {files["f_helixEmote"]} file missing')
    sys.exit()

if os.path.exists(files["f_helixReplies"]): ############################################################### helixReplies
    with open(files["f_helixReplies"], 'r') as helixRepliesFile:
        global HELIX_REPLIES
        HELIX_REPLIES = open(files["f_helixReplies"], 'r').read().split('\n')
        HELIX_REPLIES = [element for element in HELIX_REPLIES if element]
else:
    print(f'Error: {files["f_helixReplies"]} file missing')
    sys.exit()

if os.path.exists(files["f_searchEngines"]): ############################################################### searchEngines
    with open(files["f_searchEngines"], 'r') as searchEnginesFile:
        searchEngines = {}
        global SEARCH_ENGINES
        global SEARCH_ENGINES_SELECTOR
        for line in searchEnginesFile:
            engine, link = line.strip().split(" - ")
            searchEngines[engine.strip()] = link.strip()
        SEARCH_ENGINES = searchEngines
        SEARCH_ENGINES_SELECTOR = Literal[tuple(list(SEARCH_ENGINES))]
else:
    print(f'Error: {files["f_searchEngines"]} file missing')
    sys.exit()

if os.path.exists(files["f_serverToken"]): ################################################################# serverToken
    with open(files["f_serverToken"], 'r') as serverTokenFile:
        global SERVER_TOKEN
        SERVER_TOKEN = serverTokenFile.read().strip('\n')
        SERVER_TOKEN = discord.Object(id=int(SERVER_TOKEN))
else:
    print(f'Error: {files["f_serverToken"]} file missing')
    sys.exit()

class bestbot(discord.Client): ############################################################################ client setup
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
client.echoLog = {}

@client.event
async def on_ready():
    print('Bestbot online.')
    await client.change_presence(status = discord.Status.online)

########################################################################################################################
# LOCAL API
########################################################################################################################
async def echoMessage(reason, message, colour): ############################################################ echoMessage
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
# COMMANDS
########################################################################################################################
@client.tree.command(description = "Remove the most recent messages.") ########################################### clear
@app_commands.checks.has_any_role("admin", "mod")
@app_commands.describe(amount = "Number of message to delete")
async def clear(context: discord.Interaction, amount: app_commands.Range[int, 1, None]):
    await context.channel.purge(limit = amount)
    await context.response.send_message("Removed the most recent messages.")

@client.tree.command(description = "Toss a coin.") ################################################################ coin
@app_commands.describe(bet = "Wise choice", terms = "Terms of the flip")
async def coin(context: discord.Interaction, bet: Literal["heads", "tails"], terms: str):
    sides = ["heads", "tails"]
    flip = random.choice(sides)

    if flip == bet:
        embed = discord.Embed(title       = f':sunglasses: Tossed **{flip}**!',
                              description = f'Won the bet for *if {bet} {terms}*.',
                              color       = colours["green"])
    else:
        embed = discord.Embed(title       = f':sob: Tossed **{flip}**!',
                              description = f'Lost the bet for *if {bet} {terms}*.',
                              color       = colours["red"])
    await context.response.send_message(embed = embed)

@client.tree.command(description = "Convert currency.") ########################################################### conv
@app_commands.describe(amount = "Amount to convert", source = "Source currency", target = "Target currency")
async def conv(context: discord.Interaction, amount: app_commands.Range[int, 1, None],
                                             source: CURRENCY_LIST, target: CURRENCY_LIST):
    if not 'currencies.json' in os.listdir('./res'):
        await currency.retrieve_currencies(CURRENCY_KEY)

    with open('./res/currencies.json', 'r') as stored_curr:
        available_curr = json.load(stored_curr)

    if source == target:
        await context.response.send_message("Nothing to convert.", ephemeral = True)
        return

    exchanged = await currency.currency_convert(CURRENCY_KEY, amount, source, target)
    embed = discord.Embed(title       = "Currency conversion",
                          description = f'{amount:.2f} `{source}` ≈ `{target}` {exchanged:.2f}',
                          color       = colours["blue"])
    await context.response.send_message(embed = embed)

@client.tree.command(description = "Search the web.") ############################################################# find
@app_commands.describe(engine = "Search engine", query = "Search query")
async def find(context: discord.Interaction, engine: SEARCH_ENGINES_SELECTOR, query: str):
    search_input = SEARCH_ENGINES[engine] + urllib.parse.quote(query)
    embed = discord.Embed(title       = f'{engine} search results',
                          description = f'{query}\n<{search_input}>',
                          color       = colours["blue"])
    await context.response.send_message(embed = embed)

@client.tree.command(description = "Consult the Helix Fossil.") ################################################## helix
@app_commands.describe(question = "It shall answer")
async def helix(context: discord.Interaction, question: str):
    embed = discord.Embed(title       = "The fossil speaks",
                          description = f'{question}\n{HELIX_EMOTE} *{random.choice(HELIX_REPLIES)}* {HELIX_EMOTE}',
                          color       = colours["grey"])
    await context.response.send_message(embed = embed)

@client.tree.command(description = "Show the host\'s WAN IP.") ###################################################### ip
@app_commands.checks.has_role("admin")
async def ip(context: discord.Interaction):
    host_wan_ip = get('https://api.ipify.org').text
    embed = discord.Embed(title       = "Host WAN IP",
                          description = f'||`{host_wan_ip}`||',
                          color       = colours["red"])
    await context.response.send_message(embed = embed, ephemeral = True)

@client.tree.command(description = "Show the server join date.") ################################################ joined
async def joined(context: discord.Interaction):
    embed = discord.Embed(title       = "Your join date",
                          description = f"{discord.utils.format_dt(context.user.joined_at, 'D')}",
                          color       = colours["grey"])
    await context.response.send_message(embed = embed)

@client.tree.command(description = "Request a fun fact about numbers.") ######################################### number
@app_commands.describe(fact = "Type of fun fact")
async def number(context: discord.Interaction, fact: Literal["date", "math", "trivia", "year"]):
    funFact = get(f'http://numbersapi.com/random/{fact}').text
    embed = discord.Embed(title       = "Number fun fact",
                          description = funFact,
                          color       = colours["grey"])
    await context.response.send_message(embed = embed)

@client.tree.command(description = "Check network quality.") ###################################################### ping
async def ping(context: discord.Interaction):
    await context.response.send_message(f'pong! `{round(client.latency * 1000)}ms`', ephemeral = True)

@client.tree.command(description = "Request a random animal picture.") ############################################# pls
@app_commands.describe(animal = "Request type")
async def pls(context: discord.Interaction, animal: Literal["cat", "dog"]):
    URL = await cat.get(animal, CAT_KEY, random.choice(["jpg", "gif"]))
    await context.response.send_message(URL)

@client.tree.command(description = "Toggle a role.") ############################################################## role
@app_commands.describe(text = "Role to toggle")
async def role(context: discord.Interaction, text: COSMETIC_ROLES):
    request = discord.utils.get(context.guild.roles, name = text)
    if request in context.user.roles:
        await discord.Member.remove_roles(context.user, request)
        await context.response.send_message(f'Removed `{request}` role.', ephemeral = True)
    else:
        await discord.Member.add_roles(context.user, request)
        await context.response.send_message(f'Added `{request}` role.', ephemeral = True)

@client.tree.command(description = "Roll for a random number.") ################################################### roll
@app_commands.describe(max = "Max possible roll", terms = "Terms of the roll")
async def roll(context: discord.Interaction, max:  app_commands.Range[int, 1, None], terms: str):
    embed = discord.Embed(title       = f'Rolled {randint(0, max)}',
                          description = terms,
                          color       = colours["grey"])
    await context.response.send_message(embed = embed)

@client.tree.command(description = "Set a channel's slow mode.") ################################################## slow
@app_commands.describe(interval = "Delay between messages", reason = "Reason for slowdown")
@app_commands.checks.has_any_role("admin", "mod")
async def slow(context: discord.Interaction, interval: SLOWMODE_LIST, reason: str):
    await context.channel.edit(reason = reason, slowmode_delay = int(slowIntervals[interval]))
    embed = discord.Embed(title       = f'Set slow mode to {interval}',
                          description = reason,
                          color       = colours["red"])
    await context.response.send_message(embed = embed)

@client.tree.command(description = "Link towards the bot\'s source code.") ###################################### source
async def source(context: discord.Interaction):
    embed = discord.Embed(title       = "Best Source",
                          description = GH_LINK,
                          color       = colours["grey"])
    await context.response.send_message(embed = embed, ephemeral = True)

@client.tree.command(description = "Update a channel's topic.") ################################################ subject
@app_commands.describe(text = "New channel topic")
@app_commands.checks.has_any_role("admin", "mod")
async def subject(context: discord.Interaction, text: app_commands.Range[str, 1, 64]):
    await context.channel.edit(topic = text)
    embed = discord.Embed(title       = "Channel topic update",
                          description = text,
                          color       = colours["blue"])
    await context.response.send_message(embed = embed)

@client.tree.command(description = "Show the current time of a timezone.") #################################### timezone
@app_commands.describe(zone = "TZ time zone")
async def timezone(context: discord.Interaction, zone: str):
    zone = zone.title()

    try:
        time = datetime.now(ZoneInfo(zone))
    except:
        tzLink = 'https://en.wikipedia.org/wiki/List_of_tz_database_time_zones'
        await context.response.send_message(f'Incorrect timezone; see <{tzLink}>.', ephemeral = True)
        return

    time = time.strftime("%Y-%m-%d %H:%M:%S")
    embed = discord.Embed(title       = time,
                          description = zone,
                          color       = colours["blue"])
    await context.response.send_message(embed = embed)

@client.tree.command(description = "Show the system uptime.") ################################################### uptime
@app_commands.checks.has_any_role("admin", "mod")
async def uptime(context: discord.Interaction):
    with open('/proc/uptime', 'r') as uptimeFile:
        time = float(uptimeFile.readline().split()[0])

    days  = time / 86400
    hours = time / 3600 % 24

    await context.response.send_message(f'Approximate uptime: `{int(days)}d {int(hours)}h`', ephemeral = True)

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

@client.event ############################################################################################## edited echo
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
