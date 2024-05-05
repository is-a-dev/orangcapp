from __future__ import annotations

from os import environ, getenv

from dotenv import load_dotenv

load_dotenv()
import os
import traceback

import nextcord
import psycopg2
from nextcord import Intents
from nextcord.ext import commands, help_commands

prefix = "oct/" if os.getenv("TEST") else "oc/"


class OrangcBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        # self._db: psycopg2.connection = psycopg2.connect(
        #     host=getenv("DBHOST"),
        #     user=getenv("DBUSER"),
        #     port=getenv("DBPORT"),
        #     password=getenv("DBPASSWORD"),
        #     dbname=getenv("DBNAME"),
        # )
        super().__init__(*args, **kwargs)

    async def on_command_error(
        self, context: commands.Context, error: Exception
    ) -> None:
        if isinstance(error, commands.NotOwner):
            await context.send("Impersonator")
        elif isinstance(error, commands.UserInputError):
            await context.send("Such a fool can't read help")
        elif isinstance(error, commands.CommandNotFound):
            await context.send("Imagine disillusioned")
        elif isinstance(error, commands.errors.DisabledCommand):
            await context.send("Shhhhhhhh")
        else:
            await context.send("Fool")
            await super().on_command_error(context, error)


bot = OrangcBot(
    intents=Intents.all(),
    command_prefix=prefix,
    help_command=help_commands.PaginatedHelpCommand(),
    case_insensitive=True,
)
# @bot.event
# async def on_command_error(ctx, error):
#     k = await ctx.bot.create_dm(nextcord.Object(id=716134528409665586))
#     await k.send(traceback.format_exception(error))
#     print(traceback.format_exception(error))

bot.load_extension("onami")
bot.load_extension("extensions.fun")
bot.load_extension("extensions.faq")
bot.load_extension("extensions.antiphishing")
bot.load_extension("extensions.testing_functions")
bot.load_extension("extensions.nonsense")
bot.load_extension("extensions.dns")
bot.load_extension("extensions.suggestions")
bot.load_extension("extensions.delete_response")
if os.getenv("HASDB"):
    bot.load_extension("extensions.tags_reworked")
# bot.load_extension("extensions.forum")
bot.run(environ["TOKEN"])
