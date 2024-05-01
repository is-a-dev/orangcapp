from __future__ import annotations

import re
from typing import Optional

import nextcord
from nextcord.ext import commands


class LinkView(nextcord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(
            nextcord.ui.Button(label="Main Website", url="https://is-a.dev", row=1)
        )
        self.add_item(
            nextcord.ui.Button(
                label="Documentation", url="https://is-a.dev/docs", row=2
            )
        )
        self.add_item(
            nextcord.ui.Button(
                label="Register a domain!",
                url="https://github.com/is-a-dev/register",
                row=3,
            )
        )
        # self.add_item(nextcord.ui.Button(label="Help Channel", url="", row=4))


class ReportDegenModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="Degenerate Report")
        self.degen = nextcord.ui.TextInput(
            "Name of suspected degenerate", required=True
        )
        self.reason = nextcord.ui.TextInput(
            "Why they're a degenerate",
            required=True,
            style=nextcord.TextInputStyle.paragraph,
        )
        self.add_item(self.degen)
        self.add_item(self.reason)

    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user.id == 716134528409665586:
            await interaction.send(
                f"Thank you for informing me, Master. I'm sorry for my incompetence and I will deal with **{self.degen.value}** in no time. Sorry to let you down, Master."
            )
        elif interaction.user.id == 961063229168164864:
            await interaction.send("Isn't you and him one and the same?")
        else:
            await interaction.send(
                f"Actually, you would be a better degenerate than **{self.degen.value}**. Invalid report."
            )


class ReportDegenView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.message: nextcord.Message = None

    def update_msg(self, msg: nextcord.Message):
        self.message: nextcord.Message = msg

    @nextcord.ui.button(label="Report a Degenerate")
    async def report_degen(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ) -> None:
        if interaction.user.id == self.message.author.id:
            await interaction.response.send_modal(ReportDegenModal())
        else:
            await interaction.send("Fool")


class Nonsense(commands.Cog):
    """Features that exists for no reason.
    Don't ask why."""

    def __init__(self, bot: commands.Bot) -> None:
        self._bot: commands.Bot = bot

    @commands.command()
    async def links(self, ctx: commands.Context):
        """Links that are important to this service."""
        k = """Please also check those channels:
        <#991779321758896258> (for an interactive experience go to <#960446827579199488> and type `oc/faq`)
        <#1228996111390343229>
        """
        await ctx.send(view=LinkView())

    @commands.command()
    async def regex(self, ctx: commands.Context, pattern: str, string: str):
        r: Optional[re.Match] = re.fullmatch(pattern, string)
        if r:
            await ctx.message.add_reaction("✅")
        else:
            await ctx.message.add_reaction("❌")

    @commands.command()
    async def report_degenerate(self, ctx: commands.Context):
        k = ReportDegenView()
        await ctx.send("Found a degen? Report them here.", view=k)
        k.update_msg(ctx.message)


def setup(bot: commands.Bot):
    bot.add_cog(Nonsense(bot))
