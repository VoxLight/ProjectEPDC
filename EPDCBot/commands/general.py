from nextcord import Interaction, SlashOption
from nextcord.ext import commands


class General:
    """
    A class that contains general commands for the bot.

    Attributes:
        bot (commands.Bot): The bot instance.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.log.info("General commands loaded.")

    async def echo(self, 
                    interaction, 
                    message: str = SlashOption(
                        name="message", 
                        description="The message to send back.", 
                        required=True
                    )
                ):
            await interaction.send(message)


def setup(bot: commands.Bot):
    """
    Sets up the bot by registering slash commands.

    Args:
        bot (nxtcmd.Bot): The bot instance.

    Returns:
        None
    """
    # Is this hacky? Yes. Does it work? Also yes.
    # I would KILL to find a cleaner way of doing this...
    # But it's not a priority right now.
    general_slash_commands = General(bot)


    bot.slash_command(
        name="echo",
        description="Sends the same message back.",
        guild_ids=bot.config.DISCORD_DEFAULT_GUILDS
    )(general_slash_commands.echo)

    