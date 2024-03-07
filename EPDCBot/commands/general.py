from nextcord import SlashApplicationCommand, Interaction, SlashOption
from nextcord.ext import commands as nxtcmd

async def echo(interaction: Interaction, 
                message: str = SlashOption(
                    name="message", 
                    description="The message to send back.", 
                    required=True
                )
            ):
        await interaction.response.send_message(message)

def setup(bot: nxtcmd.Bot):
    # Is this hacky? Yes. Does it work? Also yes.
    # I would KILL to find a cleaner way of doing this...
    # But it's not a priority right now.
    bot.slash_command(
        name="echo",
        description="Sends the same message back.",
        guild_ids=bot.config.DISCORD_DEFAULT_GUILDS
    )(echo)
    

    