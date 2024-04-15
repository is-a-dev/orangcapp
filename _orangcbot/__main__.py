from os import environ
from dotenv import load_dotenv

load_dotenv()
import nextcord 
from nextcord.ext import commands
from nextcord import Intents
bot = commands.Bot(intents=Intents.all(), command_prefix="oc/", help_command=commands.DefaultHelpCommand())
bot.load_extension("onami")
bot.load_extension("extensions.fun")
bot.load_extension("extensions.tags")
# bot.load_extension("extensions.forum")
bot.run(environ["TOKEN"])