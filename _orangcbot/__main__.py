from os import environ
from dotenv import load_dotenv

load_dotenv()
import os
import nextcord
import traceback
from nextcord.ext import commands
from nextcord import Intents
prefix = "oct/" if os.getenv("TEST") else "oc/"
bot = commands.Bot(
    intents=Intents.all(),
    command_prefix=prefix,
    help_command=commands.DefaultHelpCommand(),
    case_insensitive=True,
)
@bot.event
async def on_command_error(ctx, error):
    k = await ctx.bot.create_dm(nextcord.Object(id=716134528409665586))
    await k.send(traceback.format_exception(error))
  
bot.load_extension("onami")
bot.load_extension("extensions.fun")
if os.getenv("HASDB"):
    bot.load_extension("extensions.tags_reworked")
# bot.load_extension("extensions.forum")
bot.run(environ["TOKEN"])
