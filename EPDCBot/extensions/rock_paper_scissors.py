from nextcord import Interaction, SlashOption
import nextcord
from nextcord.ext import commands
from views import Confirmation
import asyncio
import random
import utils
import exceptions

class RockPaperScissors(nextcord.ui.View):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    EMOJIS = {
        ROCK: "🪨",
        PAPER: "📄",
        SCISSORS: "✂️"
    }

    # rock paper scissors Information
    # A value between 0 and 1 that states how hard it is to win against the bot.
    # This value is eventually passed to the RPS_ODD_OF_WINNING function.
    RPS_DIFFICULTY_LEVEL = 1

    @staticmethod
    def RPS_odds_of_winning() -> float:
        """
        Returns the odds of winning a game of tic-tac-toe given the chance to cheat.

        args:
            chance_to_cheat: float - The percentage of the time the opponent can cheat. A value between 0 and 1.

        returns:
            float - The odds of winning the game.
        """
        # y = (1 - x) / 3
        return (1-RockPaperScissors.RPS_DIFFICULTY_LEVEL) / 3

    def __init__(self, bot: commands.Bot, player1: nextcord.Member, player2: nextcord.Member):
        super().__init__()
        self.bot = bot
        self.players = [player1, player2]
        self.player_moves = {player: None for player in self.players}



    def get_player_selection(self, player: nextcord.Member) -> int | None:
            """
            Retrieves the selection made by a player.

            Parameters:
                player (nextcord.Member): The player whose selection is to be retrieved.

            Returns:
                int | None: The selection made by the player, or None if no selection is found.
            """
            return self.player_moves.get(player)

    def set_player_selection(self, player: nextcord.Member, move: int) -> None:
        """
        Sets the move selection for a player in the game.

        Args:
            player (nextcord.Member): The player whose move selection is being set.
            move (int): The move selection for the player.

        Returns:
            None
        """
        if player in self.players:
            self.player_moves[player] = move

    def get_move_emoji(self, move: int) -> str:
        """
        Returns the emoji corresponding to the given move.

        Parameters:
        move (int): The move for which to retrieve the emoji.

        Returns:
        str: The emoji corresponding to the given move.
        """
        return self.EMOJIS.get(move)

    def get_winner(self) -> nextcord.Member | None:
        """
        Determines the winner of the rock-paper-scissors game.

        Returns:
            nextcord.Member or None: The winner of the game, or None if it's a tie.
        """
        p1_move = self.player_moves[self.players[0]]
        p2_move = self.player_moves[self.players[1]]
        if p1_move == p2_move:
            return None
        elif (p1_move == 1 and p2_move == 3) or (p1_move == 2 and p2_move == 1) or (p1_move == 3 and p2_move == 2):
            return self.players[0]
        else:
            return self.players[1]

    async def check_both_players_moved(self, interaction: Interaction) -> None:
        """
        Checks if both players have made a move.
        
        Args:
            interaction (Interaction): The interaction object representing the user interaction.
        
        Returns:
            None
        """
        if self.bot.user in self.players:

            if random.random() < RockPaperScissors.RPS_odds_of_winning():
                # Fairly select a random move.
                self.set_player_selection(self.bot.user, random.choice([1, 2, 3]))
            else:
                # Set the bot's move to the winning move against the other player's move.
                winning_moves = {1: 2, 2: 3, 3: 1}

                # A Humanized amount of delay
                await asyncio.sleep(random.random() + random.randint(0, 2))
                other_players_move = self.get_player_selection(interaction.user)
                self.set_player_selection(self.bot.user, winning_moves[other_players_move])
                await self.spawn_results(interaction)
            
        elif all(move != None for move in self.player_moves.values()):
            await self.spawn_results(interaction)

    async def spawn_results(self, interaction: Interaction) -> None:
        await interaction.followup.edit_message(message_id=interaction.message.id, content="Both players have made their move! Get ready to see the results!", view=nextcord.ui.View())
        await asyncio.sleep(2)
        content = f"""
    The results are in! Here's what each player chose:
    {self.players[0].mention}: {self.get_move_emoji(self.player_moves[self.players[0]])} vs. {self.players[1].mention}: {self.get_move_emoji(self.player_moves[self.players[1]])}
    """
        winner = self.get_winner()
        if winner is None:
            content += "\nIt's a tie!"
        else:
            content += f"\n{winner.mention} won!"
        await interaction.followup.edit_message(message_id=interaction.message.id, content=content, view=nextcord.ui.View())
        self.stop()

    @nextcord.ui.button(label="🪨", style=nextcord.ButtonStyle.secondary)
    async def rock(self, button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        if interaction.user not in self.players:
            raise exceptions.NotYoursToTouchException(f"{interaction.user.name}You are not a part of this game. see /rps to start your own!")
        
        if self.get_player_selection(interaction.user) is None:
            self.set_player_selection(interaction.user, RockPaperScissors.ROCK)
        else:
            raise exceptions.NotYourTurnException("You have already submitted a move. Please be patient and wait for your opponent to make their move.")

        await interaction.edit(content=f"{interaction.user.mention} has made their move!")
        await self.check_both_players_moved(interaction)

    @nextcord.ui.button(label="📄", style=nextcord.ButtonStyle.success)
    async def paper(self, button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        if interaction.user not in self.players:
            raise exceptions.NotYoursToTouchException(f"You are not a part of this game. see /rps to start your own!")

        if self.get_player_selection(interaction.user) is None:
            self.set_player_selection(interaction.user, RockPaperScissors.PAPER)
        else:
            raise exceptions.NotYourTurnException("You have already submitted a move. Please be patient and wait for your opponent to make their move.")

        await interaction.edit(content=f"{interaction.user.mention} has made their move!")
        await self.check_both_players_moved(interaction)

    @nextcord.ui.button(label="✂️", style=nextcord.ButtonStyle.primary)
    async def scissors(self, button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        if interaction.user not in self.players:
            raise exceptions.NotYoursToTouchException(f"You are not a part of this game. see /rps to start your own!")
        
        if self.get_player_selection(interaction.user) is None:
            self.set_player_selection(interaction.user, RockPaperScissors.SCISSORS)
        else:
            raise exceptions.NotYourTurnException("You have already submitted a move. Please be patient and wait for your opponent to make their move.")

        await interaction.edit(content=f"{interaction.user.mention} has made their move!")
        await self.check_both_players_moved(interaction)


class RockPaperScissorsCommands(commands.Cog):
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
            await interaction.edit_original_message(content=f"{interaction.user.mention}, your challenge has expired.",
                                                    view=nextcord.ui.View())

        # Declined
        elif challenge.declined:
            await interaction.edit_original_message(content=f"{interaction.user.mention}, your challenge has been declined.",
                                                    view=nextcord.ui.View())

        # Accepted
        elif challenge.accepted:
            await interaction.edit_original_message(content=f"{interaction.user.mention}, your challenge has been accepted.",
                                                    view=nextcord.ui.View())

            # Start the game!
            rps = RockPaperScissors(self.bot, *challenge.randomize_player_order())
            await interaction.edit_original_message(content="The game is starting now!",
                                            view=rps)
            await rps.wait()
            await interaction.delete_original_message(delay=5)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(RockPaperScissorsCommands(bot))
