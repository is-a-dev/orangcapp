from __future__ import annotations
from nextcord.ext import commands
import nextcord

from dotenv import load_dotenv

import psycopg2
import uuid
load_dotenv()
from os import getenv

class TagEditModal(nextcord.ui.Modal):
    def __init__(self, db: psycopg2.connection, tag_info: tuple):
        self._db: psycopg2.connection = db
        self._tag: tuple = tag_info
        super().__init__("Edit tag")

        self.my_title = nextcord.ui.TextInput(
                label="Tag Title",
                required=True,
                max_length=60,
                style=nextcord.TextInputStyle.short,
                default_value=self._tag[2]
                )
        self.add_item(self.my_title)

        self.my_content = nextcord.ui.TextInput(
                label="Tag Content",
                required=True,
                max_length = 4000,
                style=nextcord.TextInputStyle.paragraph,
                default_value=self._tag[3]
                )
        self.add_item(self.my_content)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        with self._db.cursor() as cursor:
            try:
                cursor.execute(f"UPDATE taginfo SET title='{self.my_title.value}' WHERE id='{self._tag[0]}'")
                cursor.execute(f"UPDATE taginfo SET content='{self.my_content.value}' WHERE id='{self._tag[0]}'")
            except:
                cursor.execute("ROLLBACK")

            self._db.commit()

        await interaction.response.send_message("Done", ephemeral=True)


class TagEditView(nextcord.ui.View):
    def __init__(self, ctx: comamnds.Context, db: psycopg2.connection, tag: tuple):
        super().__init__()
        self._ctx: commands.Context = ctx
        self._db: psycopg2.connection = db
        self._tag: tuple = tag
        

    @nextcord.ui.button(label="Edit tag!", style=nextcord.ButtonStyle.green)
    async def create_tag(self, button: nextcord.ui.Button, interaction: nextcord.Interaction): 
        if interaction.user.id == self._ctx.author.id:
            modal = TagEditModal(self._db, self._tag)
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message("Fool", ephemeral=True)

class TagCreationModal(nextcord.ui.Modal):
    def __init__(self, db: psycopg2.connection):
        self._db: psycopg2.connection = db
        super().__init__("Create tag")

        self.my_name = nextcord.ui.TextInput(
                label="Tag Name",
                required=True,
                max_length=60,
                style=nextcord.TextInputStyle.short,
                )

        self.add_item(self.my_name)

        self.my_title = nextcord.ui.TextInput(
                label="Tag Title",
                required=True,
                max_length=60,
                style=nextcord.TextInputStyle.short,
                )
        self.add_item(self.my_title)

        self.my_content = nextcord.ui.TextInput(
                label="Tag Content",
                required=True,
                max_length = 4000,
                style=nextcord.TextInputStyle.paragraph
                )
        self.add_item(self.my_content)

    async def callback(self, interaction: nextcord.Interaction) -> None:


        with self._db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM taginfo WHERE name='{self.my_name.value}'")
            if not cursor.fetchone():
                id = uuid.uuid4()
                try:
                    cursor.execute(f"INSERT INTO taginfo VALUES('{id.hex}', '{self.my_name.value}', '{self.my_title.value}', '{self.my_content.value}', '{str(interaction.user.id)}')")
                except:
                    cursor.execute("ROLLBACK")
                self._db.commit()
                await interaction.response.send_message("Done", ephemeral=True)
            else:
                await interaction.response.send_message("Tag already existed", ephemeral=True)
                

        # await interaction.response.send_message("Done", ephemeral=True)


class TagCreationView(nextcord.ui.View):
    def __init__(self, ctx: comamnds.Context, db: psycopg2.connection):
        super().__init__()
        self._ctx: commands.Context = ctx
        self._db: psycopg2.connection = db
        

    @nextcord.ui.button(label="Create tag!", style=nextcord.ButtonStyle.green)
    async def create_tag(self, button: nextcord.ui.Button, interaction: nextcord.Interaction): 
        if interaction.user.id == self._ctx.author.id:
            modal = TagCreationModal(self._db)
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message("Fool", ephemeral=True)

def tag_operation_check(ctx):
    return (ctx.author.get_role(830875873027817484) is not None) or ctx.author.id == 716134528409665586


class TagsNew(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot: commands.Bot = bot
        self._db: psycopg2.connection = psycopg2.connect(host=getenv("DBHOST"),

        user=getenv("DBUSER"),
        port=getenv("DBPORT"),
        password=getenv("DBPASSWORD"),
        dbname=getenv("DBNAME")
        )


    @commands.group()
    async def tag(self, ctx: commands.Context):
        pass

    @tag.command():
    async def list(self, ctx: commands.Context):
        with self._db.cursor() as cursor:
            cursor.execute("SELECT name FROM taginfo")
            await ctx.send(cursor.fetchall())

    @commands.command()
    async def find(self, ctx: commands.Context, tag_name: str = "null"):
        # print("command found")
        # print(tag_name)
        with self._db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM taginfo\nWHERE name='{tag_name}'")
            if info := cursor.fetchone():
                # print(info)
                await ctx.send(
                        embed=nextcord.Embed(
                            title=info[2],
                            description=info[3],
                            color=nextcord.Color.red()
                            ).set_footer(text=f"ID {info[0]}. Author ID: {info[4]}")
                        )
            else: await ctx.send("Fool")

    @tag.command()
    @commands.check(tag_operation_check)
    async def create(self, ctx: commands.Context):
        await ctx.send(view=TagCreationView(ctx, self._db))
    
    @tag.command()
    @commands.check(tag_operation_check)
    async def delete(self, ctx: commands.Context, tag_name: str):
        with self._db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM taginfo WHERE name='{tag_name}'")
            if info := cursor.fetchone():
                cursor.execute(f"DELETE FROM taginfo WHERE name='{tag_name}'")
                self._db.commit()
                await ctx.send("Done")
            else:
                await ctx.send("Fool")

    @tag.command()
    @commands.check(tag_operation_check)
    async def edit(self, ctx: commands.Context, tag_name: str):
        with self._db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM taginfo WHERE name='{tag_name}'")
            if info := cursor.fetchone():
                await ctx.send(f"Editing tag {tag_name}", view=TagEditView(ctx, self._db, info))
            else:
                await ctx.send("Fool")

        
def setup(bot):
    bot.add_cog(TagsNew(bot))


