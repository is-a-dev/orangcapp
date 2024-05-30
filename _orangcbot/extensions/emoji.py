from __future__ import annotations

from nextcord import Interaction, SlashOption, slash_command
from nextcord.ext import commands


class Emoji(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot: commands.Bot = bot

    @slash_command()
    async def add_emoji(
        self,
        interaction: Interaction,
    ) -> None:
        pass

    @add_emoji.subcommand()
    async def emojigg(
        self,
        interaction: Interaction,
        emoji_id: str = SlashOption(description="The emoji.gg ID", required=True),
    ) -> None: ...
