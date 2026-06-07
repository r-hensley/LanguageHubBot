import discord
from discord.ext import commands

from LanguageHubBot import LanguageHubBot


class LangHub(commands.Cog):
    def __init__(self, bot: LanguageHubBot):
        self.bot = bot
        
    


async def setup(bot: LanguageHubBot):
    await bot.add_cog(LangHub(bot))