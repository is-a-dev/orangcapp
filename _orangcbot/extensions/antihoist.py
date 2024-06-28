from __future__ import annotations

from string import ascii_letters
from typing import TYPE_CHECKING, Final

from nextcord.ext import commands
import logging

if TYPE_CHECKING:
    import nextcord

NUMBERS: Final[str] = "1234567890"
normal_characters: Final[str] = ascii_letters + NUMBERS


class AutoMod(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot: commands.Bot = bot
        try:
            assert self._bot.intents.auto_moderation is True
        except AssertionError:
            logging.getLogger("nextcord").warn(
                "auto_moderation intents is not enabled. Fix it or else no nword notifications."
            )

    @commands.Cog.listener("on_member_join")
    async def check_nickname_on_join(self, member: nextcord.Member) -> None:
        if member.display_name[0] not in normal_characters:
            await member.edit(
                nick="kid", reason="having a strong craving to be a discord ecelebrity"
            )

    @commands.Cog.listener("on_member_update")
    async def check_nickname_on_edit(
        self, _: nextcord.Member, after: nextcord.Member
    ) -> None:
        if after.display_name[0] not in normal_characters:
            await after.edit(
                nick="kid", reason="having a strong craving to be a discord ecelebrity"
            )


def setup(bot: commands.Bot) -> None:
    bot.add_cog(AutoMod(bot))
