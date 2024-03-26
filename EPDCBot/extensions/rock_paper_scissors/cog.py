import asyncio

from reusable_views import Confirmation
from EPDCBot import utils

from .rock_paper_scissors import RockPaperScissors

import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption

class RockPaperScissorsCog(commands.Cog):
    """
    A class that contains general commands for the bot.

    Attributes:
        bot (commands.Bot): The bot instance.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        utils.logger.info("Rock Paper Scissors Cog Loaded.")

    @nextcord.slash_command(
            name="rps", 
            description="Starts a game of Rock Paper Scissors with a friend.", 
            guild_ids=utils.Config.DISCORD_DEFAULT_GUILDS
    )
    async def rps(self, interaction: Interaction, member: nextcord.Member = SlashOption(
        name="member",
        description="The member to challenge.",
        required=True
    )) -> None:
        """Starts a game of Rock Paper Scissors with a friend."""

        # Don't allow the user to challenge themselves unless in debug mode
        if interaction.user == member and not self.bot.config.DEBUG_MODE:
            await interaction.response.send_message("You can't challenge yourself!!")
            return

        # Create the Challenge view object and send the challenge.
        challenge = Confirmation(interaction.user, member)
        await interaction.send(f"{member.mention} has been challenged to Rock Paper Scissors by {interaction.user.mention}.",
                               view=challenge)
        
        # Do an auto accept if the bot is challenged.
        if challenge.challengee == self.bot.user:
            await asyncio.sleep(.5)
            async with interaction.channel.typing():
                await asyncio.sleep(1.2)
                challenge.force_accept()

        # Wait for the challenge view to finish.
        await challenge.wait()

        # Timeout
        if not any([challenge.declined, challenge.accepted]):
            await interaction.edit_original_message(
                content=f"{interaction.user.mention}, your challenge has expired.",
                view=nextcord.ui.View()
            )

        # Declined
        elif challenge.declined:
            await interaction.edit_original_message(
                content=f"{interaction.user.mention}, your challenge has been declined.",
                view=nextcord.ui.View()
            )

        # Accepted
        elif challenge.accepted:
            await interaction.edit_original_message(
                content=f"{interaction.user.mention}, your challenge has been accepted.",
                view=nextcord.ui.View()
            )

            # Start the game!
            rps = RockPaperScissors(self.bot, *challenge.randomize_player_order())
            await interaction.edit_original_message(
                content="The game is starting now!",
                view=rps
            )
            await rps.wait()
            await interaction.delete_original_message(delay=5)