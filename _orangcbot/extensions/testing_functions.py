import nextcord
from nextcord.ext import commands


class Testings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot: commands.Bot = bot

    @commands.command()
    @commands.is_owner()
    async def hinder(self, ctx: commands.Context, cmd: str):
        if cmd == "hinder":
            await ctx.send("I did not expect you to be such a fool")
        else:
            command = self._bot.get_command(cmd)
            command.enabled = not command.enabled
            await ctx.send("Request satisfied, master.")

    @commands.command()
    @commands.is_owner()
    async def test_owner_perm(self, ctx: commands.Context):
        await ctx.send("Master, how can I help you?")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Testings(bot))
