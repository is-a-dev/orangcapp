from __future__ import annotations

from nextcord.ext import commands
from typing import TYPE_CHECKING
from string import ascii_letters

if TYPE_CHECKING:
    import nextcord


class Antihoist(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot: commands.Bot = bot

    @commands.Cog.listener("on_member_join")
    async def check_nickname_on_join(self, member: nextcord.Member) -> None:
        for x in member.display_name:
            if not x in ascii_letters:
                await member.edit(nick="kid", reason="attention seeking")
                return

    @commands.Cog.listener("on_member_edit")
    async def check_nickname_on_edit(
        self, _: nextcord.Member, after: nextcord.Member
    ) -> None:

        for x in after.display_name:
            if not x in ascii_letters:
                await after.edit(nick="kid", reason="attention seeking")
                return


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Antihoist(bot))
