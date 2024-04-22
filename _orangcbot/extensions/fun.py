import aiohttp
import dotenv
import nextcord
from nextcord.ext import commands
from psl_dns import PSL

dotenv.load_dotenv()
# import os
import asyncio
import datetime

_psl = PSL()
import random
from random import choice
from typing import Optional

_bonk_ans = ["Ouch!", "It hurts!", "Ohh noooo", "Pleaseeeeeee don't hurt me..."]
_morals = ["Excellent", "Good", "Normal", "Bad", "Very bad"]
# _randommer_api_key = os.getenv("RANDOMMER_API_KEY")
# def has_randommer_api_key():
#    async def predicate(ctx: comamnds.Context):
#        return _randommer_api_key != None
#    return commands.check(predicate)


# async def _request_randommer(*, params, path):
#    async with aiohttp.ClientSession() as session:
#        async with session.get(f"https://randommer.io/api/{path}", params=params, headers={"X-Api-Key": _randommer_api_key}) as response:
#            return await response.json()
class _BattleInvitation:
    def __init__(self, uid1, uid2):
        self.id = str(uid1) + str(uid2)
        self.uid1: int = uid1
        self.uid2: int = uid2


class SlapConfirmView(nextcord.ui.View):
    def __init__(self, ctx: commands.Context, invitation: _BattleInvitation):
        super().__init__()
        self._ctx: commands.Context = ctx
        self._invitation: _BattleInvitation = invitation

    @nextcord.ui.button(label="Confirm Battle", style=nextcord.ButtonStyle.blurple)
    async def _confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if self._invitation.uid2 == interaction.user.id:
            await self._ctx.send("Player 2 has accepted the Slappy Slappy battle.")
            self._ctx.bot.dispatch("battle_acceptance", self._invitation)
        else:
            await interaction.send(
                "You are not the invited competitor!", ephemeral=True
            )


class SlapView(nextcord.ui.View):
    def __init__(self, *, invitation: _BattleInvitation, ctx: commands.Context):
        super().__init__()
        self._invitation = invitation
        self._ctx = ctx
        self._message: Optional[nextcord.Message] = None
        self._user_1_count = 0
        self._user_2_count = 0

    async def timeout(self):
        asyncio.sleep(90)
        self.children[0].disabled = True
        self.stop()

    def set_message(self, message):
        self.message = message

    def determine_winner(self):
        return (
            self._invitation.uid1
            if self._user_1_count > self._user_2_count
            else self._invitation.uid2
        )

    @nextcord.ui.button(label="Slap!", style=nextcord.ButtonStyle.red)
    async def _slap(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if interaction.user.id == self._invitation.uid1:
            self._user_1_count += 1
            await interaction.response.defer()
        if interaction.user.id == self._invitation.uid2:
            self._user_2_count += 1
            await interaction.response.defer()
        else:
            await interaction.response.send_message(
                "You are not a competitor.", ephemeral=True
            )


class BonkView(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self._ctx = ctx
        self.message: Optional[nextcord.Message] = None

    def update_msg(self, msg: nextcord.Message):
        self.message = msg

    @nextcord.ui.button(label="Bonk!", style=nextcord.ButtonStyle.red)
    async def _bonk(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        print(interaction.user.id)
        print(self._ctx.author.id)
        if interaction.user.id == self._ctx.author.id:
            await self.message.edit(content=choice(_bonk_ans))
        else:
            await interaction.response.send_message("Fool", ephemeral=True)


# class RandomView(nextcord.ui.View):
#    def __init__(self, ctx, randomwhat: str):
#        super().__init__()
#        self._ctx: commands.Context = _ctx
#        self._random = randomwhat
#        self.message: Optional[nextcord.Message] = None
#
#    def update_msg(self, msg: nextcord.Message):
#        self.message = msg

#    @nextcord.ui.button("Generate a new one?", style=nextcord.ButtonStyle.green)
#    async def _generator(
#            self, button: nextcord.ui.Button, interaction: nextcord.Interaction
#            ):
#        ...

# import copy


class Fun(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.command()
    async def bonk(self, ctx):
        k = BonkView(ctx)
        msg = await ctx.send(content="Good.", view=k)
        k.update_msg(msg)

    @commands.command()
    async def areweinpsl(self, ctx):
        if _psl.is_public_suffix("is-a.dev"):
            await ctx.send("Yes, we are.")
        else:
            await ctx.send("No, we aren't.")

    @commands.command()
    async def ubdict(self, ctx: commands.Context, *, word: str):
        """contributed by vaibhav"""
        params = {"term": word}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.urbandictionary.com/v0/define", params=params
            ) as response:
                data = await response.json()
        if not data["list"]:
            return await ctx.send("No results found.")
        embed = nextcord.Embed(
            title=data["list"][0]["word"],
            description=data["list"][0]["definition"],
            url=data["list"][0]["permalink"],
            color=nextcord.Color.green(),
        )
        embed.set_footer(
            text=f"👍 {data['list'][0]['thumbs_up']} | 👎 {data['list'][0]['thumbs_down']} | Powered by: Urban Dictionary"
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def slappy(self, ctx: commands.Context, *, user: nextcord.Member):
        inv = _BattleInvitation(ctx.author.id, user.id)
        await ctx.send(
            f"<@{int(user.id)}>, <@{int(ctx.author.id)}> has invited you to a Slappy Slappy game.",
            allowed_mentions=nextcord.AllowedMentions.none(),
            view=SlapConfirmView(ctx, inv),
        )

        def check(m: _BattleInvitation):
            return m.id == inv.id

        await ctx.bot.wait_for("battle_acceptance", check=check, timeout=60)
        k = SlapView(invitation=inv, ctx=ctx)
        end = datetime.datetime.now() + datetime.timedelta(seconds=90)
        i = await ctx.send(
            f"<@{int(inv.uid1)}> and <@{inv.uid2}> has gone for a Slappy Slappy game. Press the button to score. This game ends in {nextcord.utils.format_dt(end, style='R')}.",
            allowed_mentions=nextcord.AllowedMentions.none(),
            view=k,
        )
        await k.wait()
        winner = k.determine_winner()
        await i.edit(
            f"<@{inv.uid1}> and <@{inv.uid2}> played a Slappy Slappt game in which <@{winner}> was the winner. This game has ended in {nextcord.utils.format_dt(end)}.",
            allowed_mentions=nextcord.AllowedMentions.none(),
            view=k,
        )

    @commands.command()
    async def moral(
        self, ctx: commands.Context, member: Optional[nextcord.Member] = None
    ) -> None:
        if not member:
            member = ctx.author
        if member.id in (716134528409665586, 599998971707916299):
            state = "Paragon of Virtue"
        # elif member.id == 599998971707916299:
        #     moral_edited = copy.copy(_morals).append("Paragon of Virtue")
        #     state = choice(moral_edited)
        elif member.id == 961063229168164864:
            state = "Degenerate"
        else:
            state = choice(_morals)

        await ctx.send(f"**{member.display_name}**'s moral status is **{state}**")

    @commands.command()
    async def fool(
        self, ctx: commands.Context, member: Optional[nextcord.Member] = None
    ) -> None:
        if not member:
            member = ctx.author
        if member.id == 716134528409665586:
            level = 0
        else:
            level = random.randint(0, 100)

        await ctx.send(f"**{member.display_name}** is {level}% a fool.")


def setup(bot):
    bot.add_cog(Fun(bot))
