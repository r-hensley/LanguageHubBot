import asyncio
import io
import os
import textwrap
import traceback
from contextlib import redirect_stdout

import discord
from discord.ext import commands

from LanguageHubBot import LanguageHubBot
from cogs.utils.BotUtils import bot_utils as utils

class Owner(commands.Cog):
    def __init__(self, bot: LanguageHubBot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()
    
    async def cog_check(self, ctx: commands.Context):
        owner_id = int(os.getenv("OWNER_ID"))
        
        # for main bot (not a forked bot)
        if self.bot.user.id == self.bot.constants.MAIN_FORK_ID:
            return ctx.author.id in self.bot.constants.RYRY_ALTS
        else:
            if ctx.author.id == owner_id:
                return True
            return None
    
    @commands.command(hidden=True, name='eval')
    async def _eval(self, ctx: commands.Context, *, body: str):
        # noinspection PyTypeChecker
        await ctx.invoke(self.eval_internal, seconds=15, body=body)
    
    # @commands.command(hidden=True, name='longeval')
    # async def _longeval(self, ctx: commands.Context, time, *, body: str):
    #     try:
    #         seconds = int(time)
    #     except ValueError:
    #         # length is a list of ints [days, hours, minutes]
    #         _, length = hf.parse_time(time)
    #         seconds = length[0] * 86400 + length[1] * 3600 + length[2] * 60
    #     # noinspection PyTypeChecker
    #     await ctx.invoke(self.eval_internal, seconds=seconds, body=body)
    
    async def eval_internal(self, ctx, seconds, body: str):
        """Evaluates a code"""
        
        body = body.replace('self.bot', 'bot')
        
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }
        
        env.update(globals())
        
        body = self.cleanup_code(body)
        #  these are the default quotation marks on iOS, but they cause SyntaxError: invalid character in identifier
        body = body.replace("“", '"').replace(
            "”", '"').replace("‘", "'").replace("’", "'")
        stdout = io.StringIO()
        
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}\n'
        
        try:
            exec(to_compile, env)
        except Exception as e:
            await utils.safe_send(ctx, f'```py\n{e.__class__.__name__}: {e}\n```')
            return
        
        func = env['func']
        # noinspection PyBroadException
        ret = None
        try:
            with redirect_stdout(stdout):
                ret = await asyncio.wait_for(func(), seconds)
        except asyncio.TimeoutError:
            await utils.safe_send(ctx, 'Evaluation timed out.')
        except Exception as _:
            value = stdout.getvalue()
            to_send = f'\n{value}{traceback.format_exc()}\n'
            to_send_segments = utils.split_text_into_segments(to_send, 1990)
            for segment in to_send_segments[:5]:
                await utils.safe_send(ctx, f'```py\n{segment}\n```')
            if len(to_send_segments) > 5:
                await utils.safe_send(ctx, "Output truncated. "
                                           "Showing only the first 5 messages.")
        finally:
            value = stdout.getvalue()
            # noinspection PyBroadException
            try:
                await ctx.message.add_reaction('\u2705')
            except Exception:
                pass
            
            if ret is None:
                if value:
                    segments = utils.split_text_into_segments(value, 1990)
                    for segment in segments[:5]:
                        await utils.safe_send(ctx, f'```py\n{segment}\n```')
                    if len(segments) > 5:
                        await utils.safe_send(ctx,
                                              "Output truncated. "
                                              "Showing only the first 5 messages.")
            else:
                self._last_result = ret
                segments = utils.split_text_into_segments(
                    f"{value}{ret}", 1990)
                for segment in segments[:5]:
                    await utils.safe_send(ctx, f'```py\n{segment}\n```')
                if len(segments) > 5:
                    await utils.safe_send(ctx,
                                          "Output truncated. "
                                          "Showing only the first 5 messages.")

    @staticmethod
    def cleanup_code(content):  # credit Danny
        """Automatically removes code blocks from the code."""
        # remove triple quotes + py\n
        if content.startswith("```") and content.endswith("```"):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `single quotes`
        return content.strip('` \n')
    
    @commands.command(hidden=True)
    async def reload(self, ctx, *, cogs: str):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        for cog in cogs.split():
            try:
                await self.bot.reload_extension(f'cogs.{cog}')
                if cog == 'interactions':
                    sync = self.bot.get_command('sync')
                    await ctx.invoke(sync)
            except Exception as e:
                print(ctx, cog, e)
                await self.reload_error(ctx, cog, e)
            else:
                await self.reload_success(ctx, cog)
    
    @staticmethod
    async def reload_success(ctx, cog):
        await utils.safe_send(ctx, f'**`{cog}: SUCCESS`**', delete_after=5.0)
    
    @staticmethod
    async def reload_error(ctx, cog, e):
        err = traceback.format_exc()
        err_first_line = f'{cog} - **`ERROR:`** {type(e).__name__} - {e}\n'
        remaining_char = 1990 - len(err_first_line)
        err = err_first_line + f"```py\n{err[:remaining_char]}```"
        await utils.safe_send(ctx, err)

async def setup(bot):
    await bot.add_cog(Owner(bot))
    