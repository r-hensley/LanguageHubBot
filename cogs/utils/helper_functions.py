from dataclasses import dataclass, field
from typing import Optional


class Here:
    def __init__(self):
        from LanguageHubBot import LanguageHubBot
        self.bot: Optional[LanguageHubBot] = None


here = Here()


def setup(bot):
    """This command is run in the setup_hook function in LanguageHubBot.py"""
    global here
    if here.bot is None:
        here.bot = bot
    else:
        pass
    

@dataclass
class Constants:
    """
    Constants for the bot. Most of these will be used for hardcoded references in Ryan's main
    forked bot of LanguageHubBot. Do not change them to personal values for a forked bot.
    
    If you are forking the bot and want to test something that would require you to change these
    values, it's better to change the code that is using these values to something better.
    """
    @property
    def RYRY_ID(self) -> int:
        """The ID of Ryry013's main account."""
        return 202995638860906496
    
    @property
    def RYRY_ALTS(self) -> list[int]:
        """The IDs of Ryry013's alts (Ryry013 and Abelian)."""
        return [202995638860906496, 414873201349361664]
    
    @property
    def MAIN_FORK_ID(self) -> int:
        """The ID of the main fork of LanguageHubBot."""
        return 1367811685460611122
    
    @property
    def RAI_BOT_ID(self) -> int:
        """The ID of the Rai bot."""
        return 270366726737231884
    
    @property
    def LANGUAGE_HUB_GUILD_ID(self) -> int:
        """The ID of the LanguageHub guild."""
        return 250884834803580929
    