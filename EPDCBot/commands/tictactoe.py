from typing import List
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import nextcord
import nextcord
from nextcord.ext import commands
import random
from views import Challenge


# Defines a custom button that contains the logic of the game.
# The ['TicTacToe'] bit is for type hinting purposes to tell your IDE or linter
# what the type of `self.view` is. It is not required.
class TicTacToeButton(nextcord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=nextcord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view

        # Make sure it's the current palyer pushing the button.
        if interaction.user is not view.current_player_obj:
            return
        
        # Check if the button has already been pressed.
        if view.board[self.y][self.x] != 0:
            return
        
        # Set the button to the current player's mark.
        if view.current_player_mark == view.X:
            self.style = nextcord.ButtonStyle.danger
            self.label = "X"

        else:
            self.style = nextcord.ButtonStyle.success
            self.label = "O"

        # Disable the button and set the board.
        self.disabled = True
        view.board[self.y][self.x] = view.current_player_mark

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f"{view.players[0].mention} won!"
            elif winner == view.O:
                content = f"{view.players[1].mention} won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            await interaction.edit(content=content, view=view)
            view.stop()
            return

        # Swap and update.
        view.swap_players()

        content = f"It is now {view.current_player_obj.mention} turn."

        await interaction.edit(content=content, view=view)


# This is our actual board View
class TicTacToe(nextcord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, player1: nextcord.Member, player2: nextcord.Member):
        super().__init__()
        # player1=X, player2=O
        self.players = [player1, player2]
        self.current_player_mark = self.X
        self.current_player = 0
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))
    
    @property
    def current_player_obj(self):
        return self.players[self.current_player]
    
    def swap_players(self):
        self.current_player = int(not self.current_player)
        self.current_player_mark = self.O if self.current_player == 1 else self.X

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            if value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            if value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        if diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        if diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class TicTacToeCommands:
    """
    A class that represents the Tic Tac Toe commands for the bot.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.log.info("Tic Tac Toe Loaded.")

    async def tic(self, interaction: Interaction, 
                    member: nextcord.Member = SlashOption(
                        name="member", 
                        description="The member to challenge.", 
                        required=True
                    )
                ):
        """
        Starts a tic-tac-toe game with a friend.
        """

        # Can't challenge yourself unless in debug mode.
        if interaction.user == member and not self.bot.config.DEBUG_MODE:
            await interaction.response.send_message("You can't challenge yourself!!")
            return
        
        # Create the Challenge view object and send the challenge.
        challenge = Challenge(interaction.user, member)
        await interaction.send(f"{member.mention} has been challenged to TicTacToe by {interaction.user.mention}.", 
                               view=challenge)
        
        # Wait for the challenge view to finish then mark it for deletion.
        await challenge.wait()
        await interaction.delete_original_message(delay=5)

        # Handle for each outcome.
        # Timeout
        if not any([challenge.declined, challenge.accepted]):
            await interaction.edit_original_message(content=f"{interaction.user.mention}, your challenge has expired.", view=nextcord.ui.View())

        # Declined
        elif challenge.declined: 
            await interaction.edit_original_message(content=f"{interaction.user.mention}, your challenge has been declined.", view=nextcord.ui.View())

        # Accepted
        elif challenge.accepted: 
            await interaction.edit_original_message(content=f"{interaction.user.mention}, your challenge has been accepted.")
            await interaction.followup.send(content="The game is starting now!", view=TicTacToe(*challenge.randomize_player_order()))

        
def setup(bot: commands.Bot):
    """
    Sets up the bot by registering slash commands.

    Args:
        bot (commands.Bot): The bot instance.

    Returns:
        None
    """
    # Is this hacky? Yes. Does it work? Also yes.
    # I would KILL to find a cleaner way of doing this...
    # But it's not a priority right now.
    tictactoecommands = TicTacToeCommands(bot)


    bot.slash_command(
        name="tictactoe",
        description="Starts a game of Tic Tac Toe. (Taken from the Nextcord Docs)",
        guild_ids=bot.config.DISCORD_DEFAULT_GUILDS,
    )(tictactoecommands.tic)

    