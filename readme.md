## Bestbot
Simple Discord bot with some basic functionality that I need

---
### Running
#### Dependencies
* `python3` and `discord.py`
* A `res` directory which you must create and populate; see below
#### Steps
* The `res` directory contains private data which must be filled:
    * a `blist` file a list of blacklisted words
    * a `btoken` file with the bot's token (generated on Discord's developer portal)
    * a `cadmin` file with a text channel id from my server
    * a `croles` file with a list of cosmetic roles for the `/role` command
    * an `ehelix` file with an emote id from my server
    * You will want to use your data as necessary and/or update the bot
* Run with `Python 3`
* Use the bot with the `/` prefix; see `/help` once online (unless you already read the code)

### Todo
* Elegant error handling in case required `res` files are missing
* Many things could have been done in a less barbaric way

---
### License
Copyright © 2020 Denis Isai

Licensed under the GPLv3: http://www.gnu.org/licenses/gpl-3.0.html
