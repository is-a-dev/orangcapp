from __future__ import annotations


from nextcord.ext import commands


class SubdomainNameConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        argument = argument.lower()
        if argument.endswith(".is-a.dev"):
            return argument[:-9]
        return argument
