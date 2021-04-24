## Bestbot
Simple Discord bot with basic functionality

---
### Running
#### Dependencies
* `python3` and `discord.py`
* A `res` directory which you must create and populate; see below
#### Steps
* The `res` directory contains private data which must be filled:
    * a `blacklist` file containing a list of blacklisted words
    * a `botToken` file with the bot's token (generated on Discord's developer portal)
    * a `channelAdmin` file with a text channel ID for `/ip`
    * a `cosmeticRoles` file with a list of cosmetic roles for `/role`
    * a `currencyCache` file with the API key for `/conv` generated [here](https://www.currencyconverterapi.com/)
    * a `catCache` file with the API key for `/meow` generated [here](https://thecatapi.com/)
    * an `emoteHelix` file with the Helix emote for `/helix`
    * a `helixReplies` file with a list of replies for `/helix`
    * You will want to use your data as necessary and/or update the bot
* Run with `Python 3`
* Use the bot with the `/` prefix; see `/help` once online (unless you already read the code)

### Todo
* Some things should be reworked in a less barbaric way

### Credits
* https://www.currencyconverterapi.com/ for the currency conversion API

---
### License
Copyright © 2021 Denis Isai

Licensed under the GPLv3: http://www.gnu.org/licenses/gpl-3.0.html
