from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from nextcord import Colour, Embed, Interaction, SlashOption, slash_command
from nextcord.errors import InteractionResponded
from nextcord.ext import application_checks, commands

# from models.basecog import BaseCog

if TYPE_CHECKING:
    from nextcord import TextChannel


class Suggestion(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.suggestion_channel = 1236200920317169695

    suggestion_mode = ["the server", "the service"]

    @slash_command(name="suggestion")
    async def _suggestion(self, interaction: Interaction):
        pass

    @_suggestion.subcommand(
        name="suggest", description="We'd love to hear your suggestion!"
    )
    async def _suggest(
        self,
        interaction: Interaction,
        for_: str = SlashOption(
            name="for", description="What do you want to suggest for?", required=True
        ),
        suggestion: str = SlashOption(
            name="suggestion", description="Write your suggestion here.", required=True
        ),
    ):
        if for_ == "the server":
            embed = Embed(
                title="Server Suggestion", description=suggestion, colour=Colour.red()
            )
            embed.set_footer(
                text=f"By {str(interaction.user)} (ID {interaction.user.id})"
            )

        if for_ == "the service":
            embed = Embed(
                title="Service Suggestion", description=suggestion, colour=Colour.red()
            )
            embed.set_footer(
                text=f"By {str(interaction.user)} (ID {interaction.user.id})"
            )

        channel = interaction.guild.get_channel(self.suggestion_channel)
        message = await channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        log_channel = self.bot.get_channel(955105139461607444)
        await log_channel.send(f"{str(interaction.user)} has suggested {suggestion}.")
        await interaction.send(
            f"You can now see your suggestion in {channel.mention}.",
            ephemeral=True,
        )

    @_suggest.on_autocomplete("for_")
    async def _on_suggest_for_autocomplete(self, interaction: Interaction, for_: str):
        with suppress(InteractionResponded):
            if not for_:
                await interaction.response.send_autocomplete(self.suggestion_mode)

            nearest_mode = [
                mode
                for mode in self.suggestion_mode
                if for_.lower().startswith(mode.lower())
            ]
            await interaction.response.send_autocomplete(nearest_mode)

    @_suggestion.subcommand(
        name="deny", description="[MAINTAINER ONLY] disapprove the suggestion :("
    )
    @application_checks.has_permissions(administrator=True)
    async def _deny(
        self,
        interaction: Interaction,
        messageId=SlashOption(
            name="message_id", description="Message to deny", required=True
        ),
        why: str = SlashOption(
            name="why", description="Why did you deny this request?", required=True
        ),
    ):
        channel = interaction.guild.get_channel(self.suggestion_channel)
        message = await channel.fetch_message(messageId)
        embed = message.embeds[0]
        embed.add_field(name=f"Denied by {str(interaction.user)}", value=why)
        await message.edit(embed=embed)
        await interaction.send("Done.")

    @_suggestion.subcommand(
        name="approve", description="[MAINTAINER ONLY] approve the suggestion :)"
    )
    @application_checks.has_permissions(administrator=True)
    async def _approve(
        self,
        interaction: Interaction,
        messageId: str = SlashOption(
            name="message_id", description="Message to approve", required=True
        ),
        why: str = SlashOption(
            name="why", description="Why did you deny this request?", required=False
        ),
    ):
        channel = self.bot.get_channel(self.suggestion_channel)
        message = await channel.fetch_message(messageId)
        embed = message.embeds[0]
        embed.add_field(name=f"Approved by {str(interaction.user)}", value=why)
        await message.edit(embed=embed)

        await interaction.send("Done.")


def setup(bot):
    bot.add_cog(Suggestion(bot))
