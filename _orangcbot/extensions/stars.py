from __future__ import annotations

import os
from typing import Final, Optional

import aiohttp
import nextcord
from nextcord.ext import commands, tasks


async def request(*args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(*args, **kwargs) as ans:
            return await ans.json(content_type=None)


class Stars(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot: commands.Bot = bot
        self.STAR_CHANNEL_ID: Final[int] = 1248483372242829313
        self.update_star.start()

    def cog_unload(self) -> None:
        self.update_star.stop()

    @tasks.loop(minutes=10)
    async def update_star(self):
        if os.getenv("TEST"):
            return
        data = await request(
            "GET",
            "https://api.github.com/repos/is-a-dev/register",
        )
        channel: Optional[nextcord.VoiceChannel] = self._bot.get_channel(
            self.STAR_CHANNEL_ID
        )
        if channel is not None:
            await channel.edit(name=f"{data.get("stargazers_count")} ⭐")
        else:
            return


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Stars(bot))
