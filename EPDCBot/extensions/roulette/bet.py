from typing import (
    Any, List
)


class RouletteBet:
    """
    Represents a bet in the roulette game. Bet validity relies on the user inputting the 
    correct range of numbers. For example, RouletteBet(wheel, 500, [3,4,6,7]) is legal in 
    our context, but invalid at a real roulette table.

    Parameters
    ----------
    roulette : Any
        The roulette wheel object.
    amount : float
        The amount of money the user is placing on this bet.
    bet : List[int]
        The numbers the user is betting on. Macros exist in roulette.bet_groups for Red, Black, Even, etc.

    """
    def __init__(self, amount: float, numbers: List[int]):
        self.amount = amount
        self.numbers = numbers

    def __str__(self):
        return f"${self.amount:,}"
    
class RouletteBetGroups:
    """
    Represents number groupings for different roulette bets.
    Smaller groups that are made from individual numbers are not included.
    i.e. streets, splits, corners, etc.
    """
    @staticmethod
    def EVEN(amount: int) -> RouletteBet:
        return RouletteBet(amount, [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36])

    @staticmethod
    def ODD(amount: int) -> RouletteBet:
        return RouletteBet(amount, [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35])

    @staticmethod
    def RED(amount: int) -> RouletteBet:
        return RouletteBet(amount, [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36])

    @staticmethod
    def BLACK(amount: int) -> RouletteBet:
        return RouletteBet(amount, [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35])


    @staticmethod
    def __DOZEN(amount: int, step: int) -> RouletteBet:
        return RouletteBet(amount, list(range(1 + 12 * step, 13 + 12 * step)))

    @staticmethod
    def FIRST_DOZEN(amount: int) -> RouletteBet:
        return RouletteBetGroups.__DOZEN(amount, 0)

    @staticmethod
    def SECOND_DOZEN(amount: int) -> RouletteBet:
        return RouletteBetGroups.__DOZEN(amount, 1)

    @staticmethod
    def THIRD_DOZEN(amount: int) -> RouletteBet:
        return RouletteBetGroups.__DOZEN(amount, 2)

    FIRST_HALF = [
        number for number in range(1, 19)
    ]

    SECOND_HALF = [
        number for number in range(19, 37)
    ]

        