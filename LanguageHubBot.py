import os
from typing import Optional

from dotenv import load_dotenv

import discord
from discord.ext.commands import Bot

from cogs.utils import helper_functions as hf

intents = discord.Intents.none()
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.messages = True
intents.guild_reactions = True
intents.message_content = True

dir_path = os.path.dirname(os.path.realpath(__file__))

# if no .env file exists, create one
if not os.path.exists(f"{dir_path}/.env"):
    txt = ("BOT_TOKEN=\n"
           "TRACEBACK_LOGGING_CHANNEL=\n"
           "BOT_TEST_CHANNEL=\n"
           "OWNER_ID=")
    with open(f'{dir_path}/.env', 'w', encoding='utf-8') as f:
        f.write(txt)
    print("I've created a .env file for you, go in there and put your bot token in the file, "
          "as well as a spot to put a channel ID for a channel for logging tracebacks.\n")
    exit()
    
# Credentials
load_dotenv(f'{dir_path}/.env')

if not os.getenv("BOT_TOKEN"):
    raise discord.LoginFailure(
        "You need to add your bot token to the .env file in your bot folder.")
if not os.getenv("TRACEBACK_LOGGING_CHANNEL") or not os.getenv("BOT_TEST_CHANNEL"):
    raise discord.LoginFailure("Add the IDs for a logging channel and a tracebacks channel into the .env file "
                               "in your bot folder.")

# Change these two values to channel IDs in your testing server if you are forking the bot
TRACEBACK_LOGGING_CHANNEL = int(os.getenv("TRACEBACK_LOGGING_CHANNEL"))
BOT_TEST_CHANNEL = int(os.getenv("BOT_TEST_CHANNEL"))


class LanguageHubBot(Bot):
    def __init__(self):
        super().__init__(description="Bot by Ryry013",
                         intents=intents,
                         command_prefix=',')
        self.constants: Optional[hf.Constants] = None

    async def setup_hook(self):
        # Set up helper functions file with the bot instance
        hf.setup(self)
        self.constants = hf.Constants()
        
        initial_extensions = ['cogs.main']

        # cogs.background is loaded in main.py
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                e.add_note(f'Failed to load {extension}')
                raise
            else:
                print(f"Loaded {extension}")


bot = LanguageHubBot()


@bot.event
async def on_message(msg: discord.Message):
    # Erase all message content from all users other than bot owner and bot itself
    # For user privacy purposes (this bot does not want to store any user data)
    if msg.author.id not in [bot.user.id, *bot.constants.RYRY_ALTS]:
        msg.content = ""
    
    await bot.process_commands(msg)


def run_bot():
    
    key = os.getenv("BOT_TOKEN")
    
    # a normal key is 71 characters long
    # A little bit of a deterrent from my token instantly being used
    # if the .env file gets leaked somehow
    RYRY_ID = 202995638860906496
    if len(key) == 71 and os.getenv("OWNER_ID") == str(RYRY_ID):
        key = key + '4'
    
    bot.run(key)


def main():
    run_bot()


if __name__ == '__main__':
    main()
