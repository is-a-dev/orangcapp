from nextcord.ext import commands

import nextcord
class Tags(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
    
    @commands.command()
    async def nohelp(self, ctx):
        if ctx.channel.id == 830872854677422153:
            embed = nextcord.Embed(
                title= "Please... this is not a help channel",
                description = open("texts/nohelp.txt").read(),
                color=nextcord.Colour.red()
            )
            await ctx.send(embed=embed)
        else:
            msg = await ctx.send("You fool.")
            await msg.delete()
    


def setup(bot):
    bot.add_cog(Tags(bot))