from __future__ import annotations

import black
import nextcord
from nextcord import Interaction, SlashOption, slash_command, ui
from nextcord.ext import commands


class FormatModal(ui.Modal):
    def __init__(self) -> None:
        self.code = ui.TextInput(
            label="Code to format",
            style=nextcord.TextInputStyle.paragraph,
            required=True,
        )
        self.add_item(self.code)
        super().__init__(title="Format code", timeout=900)

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        response = black.format_str(self.code.value)  # type: ignore -- it is required lmao
        await interaction.send(
            embed=nextcord.Embed(
                title="Formatted code",
                description=f"`{response}`",
                color=nextcord.Color.green(),
            )
        )


class Format(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot: commands.Bot = bot

    @slash_command()
    async def format_code(self, interaction: Interaction) -> None:  # type: ignore
        pass

    @format_code.subcommand(name="black")
    async def black_(
        self,
        interaction: Interaction,
        code=SlashOption(description="Code to format", required=False),
    ) -> None:
        """Format code with Black."""
        if not code:
            return await interaction.response.send_modal(FormatModal())
        await interaction.response.defer()

        response = black.format_str(code, mode=black.Mode())
        await interaction.send(
            embed=nextcord.Embed(
                title="Formatted code",
                description=f"```{response}```",
                color=nextcord.Color.green(),
            )
        )


def setup(bot: commands.Bot):
    bot.add_cog(Format(bot))
    return
