from nextcord import Interaction, SlashOption
import nextcord
from nextcord.ext import commands
from views import Challenge

import asyncio


class RockPaperScissors(nextcord.ui.View):
    NO_SELECTION    = 0
    ROCK            = 1
    PAPER           = 2
    SCISSORS        = 3
    MOVES = [
        ROCK, 
        PAPER, 
        SCISSORS
    ]
    EMOJIS = {
        ROCK:       "🪨",
        PAPER:      "📄",
        SCISSORS:   "✂️"
    }


    def __init__(self, bot: commands.Bot, player1: nextcord.Member, player2: nextcord.Member):
        super().__init__()
        self.bot = bot
        self.players = [player1, player2]
        self.player1_move_selected = RockPaperScissors.NO_SELECTION
        self.player2_move_selected = RockPaperScissors.NO_SELECTION

    
    def get_player_selection(self, player: nextcord.Member) -> int | None:
        if player not in self.players:
            return None
        elif player == self.players[0]:
            return self.player1_move_selected
        else:
            return self.player2_move_selected
        

    def set_player_selection(self, player: nextcord.Member, move: int) -> None:
        if player not in self.players:
            return
        elif player == self.players[0]:
            self.player1_move_selected = move
        else:
            self.player2_move_selected = move


    def get_move_emoji(self, move: int) -> str:
        return RockPaperScissors.EMOJIS[move]
    

    def get_winner(self) -> nextcord.Member:
        if self.player1_move_selected == self.player2_move_selected:
            return None
        elif self.player1_move_selected == RockPaperScissors.ROCK and self.player2_move_selected == RockPaperScissors.SCISSORS:
            return self.players[0]
        elif self.player1_move_selected == RockPaperScissors.PAPER and self.player2_move_selected == RockPaperScissors.ROCK:
            return self.players[0]
        elif self.player1_move_selected == RockPaperScissors.SCISSORS and self.player2_move_selected == RockPaperScissors.PAPER:
            return self.players[0]
        else:
            return self.players[1]


    async def check_both_players_moved(self, interaction: Interaction):
        if self.player1_move_selected != RockPaperScissors.NO_SELECTION and \
        self.player2_move_selected != RockPaperScissors.NO_SELECTION:
            await self.spawn_results(interaction)


    async def spawn_results(self, interaction: Interaction):
        await interaction.followup.edit_message(message_id=interaction.message.id, content="Both players have made their move! Get ready to see the results!", view=nextcord.ui.View())
        await asyncio.sleep(3)
        content = f"""
The results are in! Here's what each player chose:
{self.players[0].mention}: {self.get_move_emoji(self.player1_move_selected)} vs. {self.players[1].mention}: {self.get_move_emoji(self.player2_move_selected)}
"""
        winner = self.get_winner()
        if winner is None:
            content += "\nIt's a tie!"
        else:
            content += f"\n{winner.mention} won!"
        await interaction.followup.edit_message(message_id=interaction.message.id, content=content, view=nextcord.ui.View())
        self.stop()


    @nextcord.ui.button(label="🪨", style=nextcord.ButtonStyle.secondary)
    async def rock(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if  interaction.user not in self.players:
            return
        if self.get_player_selection(interaction.user) is RockPaperScissors.NO_SELECTION:
            self.set_player_selection(interaction.user, RockPaperScissors.ROCK)
            self.bot.log.info(f"{interaction.user} has selected Rock.")

        await interaction.edit(content=f"{interaction.user.mention} has made their move!")
        await self.check_both_players_moved(interaction)


    @nextcord.ui.button(label="📄", style=nextcord.ButtonStyle.success)
    async def paper(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user not in self.players:
            return
        if self.get_player_selection(interaction.user) is RockPaperScissors.NO_SELECTION:
            self.set_player_selection(interaction.user, RockPaperScissors.PAPER)
            self.bot.log.info(f"{interaction.user} has selected Paper.")

        await interaction.edit(content=f"{interaction.user.mention} has made their move!")
        await self.check_both_players_moved(interaction)


    @nextcord.ui.button(label="✂️", style=nextcord.ButtonStyle.primary)
    async def scissors(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user not in self.players:
            return
        if self.get_player_selection(interaction.user) is RockPaperScissors.NO_SELECTION:
            self.set_player_selection(interaction.user, RockPaperScissors.SCISSORS)
            self.bot.log.info(f"{interaction.user} has selected Scissors.")

        await interaction.edit(content=f"{interaction.user.mention} has made their move!")
        await self.check_both_players_moved(interaction)


class RockPaperScissorsCommands:
    """
    A class that contains general commands for the bot.

    Attributes:
        bot (commands.Bot): The bot instance.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.log.info("Tic Tac Toe Loaded.")


    async def rps(self, interaction: Interaction, 
                    member: nextcord.Member = SlashOption(
                        name="member", 
                        description="The member to challenge.", 
                        required=True
                    )
                ):
        """Starts a tic-tac-toe game with a friend."""

        # Dont allow the user to challenge themselves unless in debug mode
        if interaction.user == member and not self.bot.config.DEBUG_MODE:
            await interaction.response.send_message("You can't challenge yourself!!")
            return
        
        # Create the Challenge view object and send the challenge.
        challenge = Challenge(interaction.user, member)
        await interaction.send(f"{member.mention} has been challenged to Rock Paper Scissors by {interaction.user.mention}.", 
                               view=challenge)
        
        # Wait for the challenge view to finish and mark it for deletion
        await challenge.wait()
        await interaction.delete_original_message(delay=5)

        # Timeout
        if not any([challenge.declined, challenge.accepted]):
            await interaction.edit_original_message(content=f"{interaction.user.mention}, your challenge has expired.", view=nextcord.ui.View())

        # Declined
        elif challenge.declined: 
            await interaction.edit_original_message(content=f"{interaction.user.mention}, your challenge has been declined.", view=nextcord.ui.View())

        # Accepted
        elif challenge.accepted: 
            await interaction.edit_original_message(content=f"{interaction.user.mention}, your challenge has been accepted.", view=nextcord.ui.View())

            # Send a new message to start the game
            await interaction.followup.send(content="The game is starting now!", view=RockPaperScissors(self.bot, *challenge.randomize_player_order()))
            

def setup(bot: commands.Bot):
    rps_commands = RockPaperScissorsCommands(bot)


    bot.slash_command(
        name="rps",
        description="Starts a game of RockPaperScissors.",
        guild_ids=bot.config.DISCORD_DEFAULT_GUILDS,
    )(rps_commands.rps)

    