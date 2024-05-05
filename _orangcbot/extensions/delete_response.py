from __future__ import annotations

from nextcord.ext import commands
import nextcord


class DeleteResponse(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event: nextcord.RawReactionActionEvent) -> None:
        if event.event_type == "REACTION_ADD":
            # print(event.emoji == "<:delete:1236642973576331328>")
            if str(event.emoji) == "<:delete:1236642973576331328>":
                n = await self._bot.get_channel(event.channel_id).fetch_message(event.message_id)
                if self._bot.get_user(event.user_id).bot == False:
                    if n.author.id == self._bot.user.id:
                        await n.delete()
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass

def setup(bot: commands.Bot) -> None:
    bot.add_cog(DeleteResponse(bot))
