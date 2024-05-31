from __future__ import annotations

import asyncio
from typing import Final

import nextcord
from nextcord.ext import commands

STAFF_ROLE_ID: Final[int] = 1197475623745110109
ONEWORD_CHANNEL_ID: Final[int] = 1225794824649838612


class Oneword(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message) -> None:
        if message.author.bot:
            return
        if message.author.get_role(STAFF_ROLE_ID):  # type: ignore[reportAttributeAccessIssue]
            return  # type: ignore[reportAttributeAccessIssue]
        if message.channel.id != ONEWORD_CHANNEL_ID:
            return
        if " " in message.content:
            await message.delete()
            r = await message.channel.send(
                "Message which have space(s) are not allowed."
            )
            await asyncio.sleep(5)
            await r.delete()

    @commands.Cog.listener()
    async def on_message_edit(
        self, before: nextcord.Message, after: nextcord.Message
    ) -> None:
        if after.channel.id != ONEWORD_CHANNEL_ID:
            return
        if before.id != after.id:
            return
        if after.author.get_role(STAFF_ROLE_ID):  # type: ignore[reportAttributeAccessIssue]
            return  # type: ignore[reportAttributeAccessIssue]
        if " " in after.content:
            await after.delete()
            r = await after.channel.send("Good try, kid.")
            await asyncio.sleep(5)
            await r.delete()

    @commands.Cog.listener()
    async def on_message_delete(self, message: nextcord.Message) -> None:
        if message.author.bot:
            return
        if " " in message.content:
            return
        if message.channel.id == ONEWORD_CHANNEL_ID:
            await message.channel.send(
                f"{message.author.mention}: {message.content}",
                allowed_mentions=nextcord.AllowedMentions.none(),
            )


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Oneword(bot))
