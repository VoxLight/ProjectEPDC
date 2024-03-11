import nextcord
import random

from typing import List

class Challenge(nextcord.ui.View):
    
    def __init__(self, challenger: nextcord.Member, challengee: nextcord.Member):
        super().__init__()
        self.challenger = challenger
        self.challengee = challengee
        self.accepted = False
        self.declined = False
        self.timeout = 5 * 60  # 5 minutes

    # This is used when we want to get a random order of players.
    # This is common when creating challenges for turn based games.
    def randomize_player_order(self) -> List[nextcord.Member]:
            """
            Shuffles the list of players and returns the shuffled list.

            Returns:
                List[nextcord.Member]: The shuffled list of players.
            """
            players = [self.challenger, self.challengee]
            random.shuffle(players)
            return players


    @nextcord.ui.button(label="Accept", style=nextcord.ButtonStyle.success)
    async def accept(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user != self.challengee:
            return
        
        # Mark this chlalenge as accepted.
        self.accepted = True

        # Stop the challenge view.
        self.stop()

    @nextcord.ui.button(label="Decline", style=nextcord.ButtonStyle.danger)
    async def decline(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user != self.challengee:
            return
        
        # Mark this challenge as declined
        self.declined = True

        # Stop the challenge view.
        self.stop()