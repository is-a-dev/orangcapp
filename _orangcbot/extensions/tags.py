from nextcord.ext import commands

import nextcord

nohelp = """
Hey you! This is not a help channel!\n
We have a help channel for a reason, <#1155589227728339074>.\n
Please use that as a help channel. We need you to open a thread, even if it is a tiny problem.\n
So... **Enjoy troll answers past this message and take them with a pinch of salt. The action of following any help in this channel past this message is at your own risk. You've been warned.**\n
Please check the [is-a.dev docs](https://www.is-a.dev/docs/)\n
Have fun!"""
class Tags(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
    
    @commands.command()
    async def nohelp(self, ctx):
        if ctx.channel.id in [830872854677422153, 1057228967972716584]:
            embed = nextcord.Embed(
                title= "Please... this is not a help channel",
                description = nohelp,
                color=nextcord.Colour.red()
            )
            await ctx.send(embed=embed)
        else:
            msg = await ctx.send("You fool.")
            await msg.delete()
    


def setup(bot):
    bot.add_cog(Tags(bot))