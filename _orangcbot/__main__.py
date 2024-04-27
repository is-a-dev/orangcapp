from __future__ import annotations
from os import environ, getenv
from dotenv import load_dotenv

load_dotenv()
import os
import nextcord
import traceback
from nextcord.ext import commands
from nextcord import Intents
import psycopg2

prefix = "oct/" if os.getenv("TEST") else "oc/"

class OrangcBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        self._db: psycopg2.connection = psycopg2.connect(
            host=getenv("DBHOST"),
            user=getenv("DBUSER"),
            port=getenv("DBPORT"),
            password=getenv("DBPASSWORD"),
            dbname=getenv("DBNAME"),
        )
        super().__init__(*args, **kwargs)

    async def on_command_error(self, context: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.NotOwner):
            await context.send("Impersonator")
        elif isinstance(error, commands.UserInputError):
            await context.send("Such a fool can't read help")
        elif isinstance(error, commands.CommandNotFound):
            await context.send("Imagine disillusioned")
        else:
            await context.send("Fool")
            await super().on_command_error(context, error)

    async def on_message(self, message: nextcord.Message) -> None:
        if not os.getenv("HASDB"): return
        if os.getenv("NO_SPAWN_TAG"): return 
        if message.content.startswith("^"):
            with self._db.cursor() as cursor:
                cursor.execute(f"SELECT * FROM taginfo\nWHERE name='{message.content[1:]}'")
                if info := cursor.fetchone():
                    # print(info)
                    await message.channel.send(
                        embed=nextcord.Embed(
                            title=info[2], description=info[3], color=nextcord.Color.red()
                        ).set_footer(text=f"ID {info[0]}. Author ID: {info[4]}")
                    )
                else:
                    pass
        else:
            await super().on_message(message)

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
