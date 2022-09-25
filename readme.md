## Bestbot
Simple Discord bot with basic(-ish) functionality

---
### Running
#### Dependencies
* `python3` and `discord.py`
* A `res` directory which you must create and populate; see below
#### Steps
* The `res` directory contains private data which must be filled:
    * a `blacklist` file containing a list of blacklisted words
    * a `botToken` file with the bot's token (generated on Discord's developer portal)
    * a `serverToken` file with the server ID
    * a `channelEcho` file with a text channel ID for the deleted/edited message tracker
    * a `cosmeticRoles` file with a list of cosmetic roles for `/role`
    * a `currencyKey` file with the API key for `/conv` generated [here](https://www.currencyconverterapi.com/)
    * a `catKey` file with the API key for `/pls` generated [here](https://thecatapi.com/) or [here](https://thedogapi.com/)
    * an `emoteHelix` file with the Helix emote for `/helix`
    * a `helixReplies` file with a list of replies for `/helix`
    * You will want to use your data as necessary and/or update the bot
* Run with `Python 3`
* Use the bot with the `/` prefix; see `/help` once online (unless you already read the code)

### Credits
* https://www.currencyconverterapi.com/ for the currency conversion API
* https://thecatapi.com/ for the cat picture API
* https://thedogapi.com/ for the dog picture API

---
### License
Copyright © 2022 Denis Isai

Licensed under the GPLv3: http://www.gnu.org/licenses/gpl-3.0.html
