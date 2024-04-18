from nextcord.ext import commands
from psl_dns import PSL
import nextcord
import aiohttp

_psl = PSL()
from typing import Optional
from random import choice

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
    
    @commands.command()
    async def ubdict(self, ctx: commands.Context, *, word: str):
        """contributed by vaibhav"""
        params = {"term": word}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.urbandictionary.com/v0/define", params=params
            ) as response:
                data = await response.json()
        if not data["list"]:
            return await ctx.send("No results found.")
        embed = nextcord.Embed(
            title=data["list"][0]["word"],
            description=data["list"][0]["definition"],
            url=data["list"][0]["permalink"],
            color=nextcord.Color.green(),
        )
        embed.set_footer(
            text=f"👍 {data['list'][0]['thumbs_up']} | 👎 {data['list'][0]['thumbs_down']} | Powered by: Urban Dictionary"
        )
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Fun(bot))
