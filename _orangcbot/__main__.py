from os import environ
from dotenv import load_dotenv

load_dotenv()

from nextcord.ext import commands
bot = commands.Bot()

bot.load_extension("extensions.fun")

bot.run(environ["TOKEN"])