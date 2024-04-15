import nextcord
from nextcord.ext import commands
from psl_dns import PSL

_psl = PSL()
from random import choice
from typing import Optional

_bonk_ans = ["Ouch!", "It hurts!", "Ohh noooo", "Pleaseeeeeee don't hurt me..."]


class View(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self._ctx = ctx
        self.message: Optional[nextcord.Message] = None

    def update_msg(self, msg: nextcord.Message):
        self.message = msg

    @nextcord.ui.button(label="Bonk!", style=nextcord.ButtonStyle.red)
    async def _bonk(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if interaction.user.id == self._ctx.author.id:
            await self.message.edit(content=choice(_bonk_ans))


class Fun(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.command()
    async def bonk(self, ctx):
        k = View(ctx)
        msg = await ctx.send(content="Good.", view=k)
        k.update_msg(msg)

    @commands.command()
    async def areweinpsl(self, ctx):
        if _psl.is_public_suffix("is-a.dev"):
            await ctx.send("Yes, we are.")
        else:
            await ctx.send("No, we aren't.")


def setup(bot):
    bot.add_cog(Fun(bot))
