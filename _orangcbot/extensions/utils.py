from __future__ import annotations


import nextcord
from nextcord.ui import Item

from typing import TYPE_CHECKING


class TextBasedOnlyAuthorCheck(Item):
    if TYPE_CHECKING:
        _message: nextcord.Message
        _author_id: int

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        if hasattr(self, "_message"):
            return interaction.user.id == self._message.author.id
        elif hasattr(self, "_author_id"):
            return interaction.user.id == self._author_id
        else:
            raise nextcord.ApplicationCheckFailure(
                (
                    "An `TextBasedOnlyAuthorCheck` was used but"
                    "neither `_message` or `_author_id` attribute was found."
                )
            )
