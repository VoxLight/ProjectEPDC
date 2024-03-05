class EPDCBotException(Exception):
    """Base class for exceptions in the EPDCBot package."""
    pass

class DatabaseException(EPDCBotException):
    """Exception raised for errors in the database."""
    pass