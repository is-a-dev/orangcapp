from __future__ import annotations

import random
from typing import TYPE_CHECKING

import nextcord
from dns import resolver as _dnsresolver
from nextcord.ext import commands

_blobs = [
    "<:blobcat_cute:1236176247759966298>",
    "<:blobcat_food:1236176414768762880>",
    "<:blobcat_pat:1236176350738387027>",
    "<:blobcat_present:1236175869404254209>",
    "<:blobcat_queen:1236175473168486481>",
    "<:blobcat_salute:1236175609391087646>",
    "<:blobcat_smart:1236175952891871322>",
    "<:blobcat_sup:1236175739859112048>",
    "<:blobcat_thirst:1236176039898648606>",
]


class DigSelectOption(nextcord.SelectOption):
    def __init__(self, record_name: str):
        super().__init__(
            label=record_name,
            value=record_name,
            description=f"Fetch the {record_name} record of the domain",
            emoji=random.choice(_blobs),
        )


def construct_embed(url: str, answer: str, record_type: str):
    return nextcord.Embed(
        title=f"{record_type} records for {url}",
        description=f"```{answer}```",
        color=nextcord.Color.red(),
    )


class DigDropdown(nextcord.ui.Select):
    if TYPE_CHECKING:
        _message: nextcord.Message

    def __init__(self, url: str):
        options = [
            DigSelectOption("A"),
            DigSelectOption("CNAME"),
            DigSelectOption("AAAA"),
            DigSelectOption("MX"),
            DigSelectOption("TXT"),
        ]
        self._url: str = url
        super().__init__(options=options, placeholder="What records do you want?")

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        try:
            answers = _dnsresolver.resolve(self._url, interaction.data["values"][0])
            answer = "\n".join([str(ans) for ans in answers])
        except _dnsresolver.NoAnswer:
            answer = "NOT FOUND"
        await self._message.edit(
            embed=construct_embed(self._url, answer, interaction.data["values"][0])
        )

    def update_msg(self, msg: nextcord.Message):
        self._message: nextcord.Message = msg


class DNSView(nextcord.ui.View):
    if TYPE_CHECKING:
        _message: nextcord.Message

    def __init__(self, url: str, author_id: int):
        super().__init__(timeout=600)
        self.dropdown = DigDropdown(url)
        self.add_item(self.dropdown)
        self._author_id: int = author_id

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        if interaction.user.id == self._author_id:
            return True
        else:
            await interaction.send("Fool", ephemeral=True)
            return False

    def update_msg(self, msg: nextcord.Message) -> None:
        self._message = msg
        self.dropdown.update_msg(msg)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self._message.edit(view=self)


class DNS(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot: commands.Bot = bot

    @commands.command()
    async def dig(self, ctx: commands.Context, url: str):
        """Dig an URL for its DNS records. Default to CNAME, if you want other then select in the dropdown."""
        try:
            answers = _dnsresolver.resolve(url, "CNAME")
            answer = "\n".join([str(ans) for ans in answers])
        except _dnsresolver.NoAnswer:
            answer = "NOT FOUND"
        k = DNSView(url, ctx.author.id)
        msg = await ctx.send(embed=construct_embed(url, answer, "CNAME"), view=k)
        k.update_msg(msg)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(DNS(bot))
