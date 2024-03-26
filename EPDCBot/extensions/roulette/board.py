import math

from typing import List, AnyStr
from .bet import RouletteBet

class RouletteBoard:
    DEFAULT_WHEEL_SIZE = 36

    # Used for setting payout rates
    STRAIGHT_BET_PAYOUT = 35
    """
    Represents the roulette board. This class is responsible for keeping track of all the bets
    placed on the board. It also has a method for spinning the wheel and determining the winning
    number.

    Parameters
    ----------
    extra_spaces : int, optional
        The number of extra spaces on the wheel. This is 0 by default. Changes the payout edge in favor of the house.

    """
    def __init__(self, extra_spaces: int = 0):
        self.bets: List[RouletteBet] = []
        self.extra_spaces = extra_spaces

    def calculate_bet_odds(self, bet: RouletteBet) -> float:
        """
        Calculates the odds of winning a bet. This is -not- used to determine the payout of a bet.

        Parameters
        ----------
        bet : RouletteBet
            The bet to calculate the odds for.

        Returns
        -------
        float
            The odds of the bet.

        """
        return len(bet.numbers) / (RouletteBoard.DEFAULT_WHEEL_SIZE + self.extra_spaces)

    def calculate_bet_payout(self, bet: RouletteBet) -> float:
        """
        Calculates the payout of a bet. This is -not- used to determine the odds of a bet.

        Parameters
        ----------
        bet : RouletteBet
            The bet to calculate the payout for.

        Returns
        -------
        float
            The payout of the bet.

        """
        return RouletteBoard.STRAIGHT_BET_PAYOUT // len(bet.numbers) * bet.amount

