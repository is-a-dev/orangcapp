from __future__ import annotations


from nextcord.ext import commands
import re
import urllib.parse

import asyncio 
import aiohttp
import nextcord 

class AntiPhish(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        links = re.findall(r"(https?://[^\s]+)", message.content)
        for link in links:
            async with aiohttp.ClientSession() as session:
                host = urllib.parse.urlparse(link).hostname
                async with session.get(f"https://api.phisherman.gg/v1/domains/{host}") as answer:
                    r = await answer.text()
                    # print(r)
                    if r == "true":
                        await self._bot.get_channel(955105139461607444).send(  # type: ignore[reportAttributeAccessIssue]
                                embed=nextcord.Embed(
                                    title="Phishing found",
                                    description=f"Message sender: {message.author.id}, original content: ```{message.content}```",
                                    color=nextcord.Color.red()))
                        await message.delete()
                        break

            await asyncio.sleep(1.5)
            

def setup(bot):
    bot.add_cog(AntiPhish(bot))

