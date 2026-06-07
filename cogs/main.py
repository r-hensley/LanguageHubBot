import traceback

import discord
from discord.ext import commands

from LanguageHubBot import LanguageHubBot
from cogs.utils import helper_functions as hf

async def load_cogs(bot: LanguageHubBot):
    cogs = [
        "cogs.owner",
        "cogs.langhub",
    ]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
        except Exception as e:
            print(f"Failed to load cog {cog}: {e}")
            print(traceback.print_exc())
        else:
            print(f"Loaded {cog}")

class Main(commands.Cog):
    def __init__(self, bot: LanguageHubBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await load_cogs(self.bot)
        
        print(f"Logged in as {self.bot.user.name} - {self.bot.user.id}")
        print("------")
        await self.bot.change_presence(activity=discord.Game(name="LanguageHub"))
        
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        pass
    
async def setup(bot: LanguageHubBot):
    await bot.add_cog(Main(bot))
    