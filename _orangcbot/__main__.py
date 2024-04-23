from os import environ
from dotenv import load_dotenv

load_dotenv()
import os
import nextcord
import traceback
from nextcord.ext import commands
from nextcord import Intents


prefix = "oct/" if os.getenv("TEST") else "oc/"

class OrangcBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def on_command_error(self, context: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.NotOwner):
            await context.send("Impersonator")
        elif isinstance(error, commands.UserInputError):
            await context.send("Such a fool can't read help")
        else:
            await context.send("Fool")
            await super().on_command_error(context, error)

bot = OrangcBot(
    intents=Intents.all(),
    command_prefix=prefix,
    help_command=commands.DefaultHelpCommand(),
    case_insensitive=True,
)
# @bot.event
# async def on_command_error(ctx, error):
#     k = await ctx.bot.create_dm(nextcord.Object(id=716134528409665586))
#     await k.send(traceback.format_exception(error))
#     print(traceback.format_exception(error))

bot.load_extension("onami")
bot.load_extension("extensions.fun")
if os.getenv("HASDB"):
    bot.load_extension("extensions.tags_reworked")
# bot.load_extension("extensions.forum")
bot.run(environ["TOKEN"])
