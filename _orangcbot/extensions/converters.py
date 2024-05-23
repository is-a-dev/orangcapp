from __future__ import annotations

from typing import Tuple

from nextcord.ext import commands


class SubdomainNameConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> str:
        argument = argument.lower()
        if argument.endswith(".is-a.dev"):
            return argument[:-9]
        return argument


class RGBColorTupleConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> Tuple[str]:
        return argument.split("-")  # type: ignore[reportReturnType]
