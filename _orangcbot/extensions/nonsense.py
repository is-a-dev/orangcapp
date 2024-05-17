from __future__ import annotations

import re
from typing import TYPE_CHECKING, Optional

import aiohttp
import nextcord
from nextcord.ext import commands

from .converters import SubdomainNameConverter


class DomainNotExistError(commands.CommandError):
    """Error raised when domain cannot be found."""


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


async def request(*args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(*args, **kwargs) as ans:
            if ans.status == 404:
                raise DomainNotExistError("imagine")
            return await ans.json(content_type=None)


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


class ProposeView(nextcord.ui.View):
    if TYPE_CHECKING:
        message: nextcord.Message

    def __init__(self, spouse_id: int):
        super().__init__(timeout=30)
        self._spouse_id: int = spouse_id
        self._answered: Optional[bool] = None

    def update_msg(self, msg: nextcord.Message):
        self._message = msg

    @nextcord.ui.button(label="Yes", style=nextcord.ButtonStyle.green)
    async def yes(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        for child in self.children:
            child.disabled = True
        self._answered = True
        await interaction.response.defer()
        await self._message.edit("I love you!", view=self)

    @nextcord.ui.button(label="No", style=nextcord.ButtonStyle.red)
    async def no(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        for child in self.children:
            child.disabled = True
        self._answered = True
        await interaction.response.defer()
        await self._message.edit("I hereby refuse your refusal.", view=self)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if not self._answered:
            await self._message.edit("You missed the boat. Failure.", view=self)

    async def interaction_check(self, interaction: nextcord.Interaction):
        if interaction.user.id == self._spouse_id:
            return True
        else:
            await interaction.send("Fool", ephemeral=True)
            return False


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
            await interaction.send("Fool", ephemeral=True)


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
        await ctx.send(k, view=LinkView())

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

    @commands.command()
    async def propose(self, ctx: commands.Context):
        k = ProposeView(ctx.author.id)
        i = await ctx.send("Will you marry me?", view=k)
        k.update_msg(i)

    @commands.command()
    # @commands.cooldown(3, 8, commands.BucketType.user)
    # @commands.has_role(830875873027817484)
    async def screenshot(self, ctx: commands.Context, url: str):
        await ctx.send(
            embed=nextcord.Embed(
                title="Screenshot",
                description=f"[Open in browser for fast rendering](http://image.thum.io/get/{url})",
                color=nextcord.Color.red(),
            )
        )

    def fetch_description_about_a_domain(self, data: Dict):
        parsed_contact = {}
        print(data["owner"])
        for platform, username in data["owner"].items():
            if platform == "username":
                parsed_contact["github"] = (
                    f"[{username}](https://github.com/{username})"
                )
            elif platform == "twitter":
                parsed_contact["twitter"] = (
                    f"[{username}](https://twitter.com/{username})"
                )
            elif platform == "email":
                if username != "":
                    parsed_contact["email"] = username
            else:
                # unknown contact, ignoring
                parsed_contact[platform] = username

        contact_desc = """**Contact Info**:\n"""
        for x, y in parsed_contact.items():
            contact_desc += f"**{x}**: {y}\n"

        record_desc = """**Record Info**:\n"""
        for x, y in data["record"].items():
            if x == "CNAME":
                record_desc += f"**{x}**: {y} [(visit this CNAME?)](https://{y})\n"
            else:
                record_desc += f"**{x}**: {y}\n"

        if domain_desc := data.get("description"):
            domain_desc = "**Description**: " + domain_desc + "\n"
        else:
            domain_desc = None

        if repo := data.get("repo"):
            repo_desc = "**Repository**: " + f"[here]({repo})" + "\n"
        else:
            repo_desc = None

        # do not ask about the description of this thing
        my_description = f"""
        {contact_desc}

        {record_desc}
        """
        if domain_desc is not None:
            my_description += domain_desc + "\n"
        if repo_desc is not None:
            my_description += repo_desc + "\n"
        return my_description

    @commands.command()
    async def whois(
        self, ctx: commands.Context, domain: SubdomainNameConverter
    ) -> None:
        k = nextcord.ui.View()
        k.add_item(
            nextcord.ui.Button(
                style=nextcord.ButtonStyle.url,
                url=f"https://github.com/is-a-dev/register/edit/main/domains/{domain}.json",
                label="Edit this subdomain?",
            )
        )
        try:
            data = await request(
                "GET",
                f"https://raw.githubusercontent.com/is-a-dev/register/main/domains/{domain}.json",
            )
        except DomainNotExistError:
            await ctx.send("The domain queried cannot be found. Aborting.")
            return
        embed = nextcord.Embed(
            color=nextcord.Color.red(),
            title=f"Info about {domain}.is-a.dev",
            description=self.fetch_description_about_a_domain(data),
        )
        await ctx.send(embed=embed, view=k)


def setup(bot: commands.Bot):
    bot.add_cog(Nonsense(bot))
