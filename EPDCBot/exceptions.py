from nextcord.errors import ApplicationError

class EPDCBotException(ApplicationError):
    """Base class for exceptions in the EPDCBot package."""
    pass

class DatabaseException(EPDCBotException):
    """Exception raised for errors in the database."""
    pass

class NotYoursToTouchException(EPDCBotException):
    """Exception raised when a player tries to interact with an interaction they are not a part of."""
    pass

class NotYourTurnException(EPDCBotException):
    """Exception raised when a player tries to make a move when it is not their turn."""
    pass