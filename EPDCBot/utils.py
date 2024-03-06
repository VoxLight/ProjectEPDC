import os
import logging


class Config:

    def __init__(self):
        # The following environment variables are set in a .env file. See .env.example.
        self.DB_USER = os.environ.get('POSTGRES_USER')
        self.DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
        self.DB_NAME = os.environ.get('POSTGRES_DB')
        self.DB_HOST = os.environ.get('POSTGRES_HOST')
        self.DB_PORT = os.environ.get('POSTGRES_PORT')

    @property
    def DATABASE_URI(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}" 


def get_logger():
    # Create a logger object.
    logger = logging.getLogger('EPDCBot')

    # Set the level of this logger. 
    logger.setLevel(logging.DEBUG)

    # Create a file handler for outputting log messages to a file
    fh = logging.FileHandler('/app/logs/bot.log')

    # Create a console handler for outputting log messages to the console
    ch = logging.StreamHandler()

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger



