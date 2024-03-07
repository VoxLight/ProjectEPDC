import os
import logging
from typing import List


class Config:
    """
    Represents the configuration settings for the application.
    """

    def __init__(self):
        # The following environment variables are set in a .env file. See .env.example.

        # Database connection information
        self.DB_USER     = os.environ.get('POSTGRES_USER')
        self.DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
        self.DB_NAME     = os.environ.get('POSTGRES_DB')
        self.DB_HOST     = os.environ.get('POSTGRES_HOST')
        self.DB_PORT     = os.environ.get('POSTGRES_PORT')

        # Discord information
        self.DISCORD_BOT_TOKEN                 = os.environ.get('DISCORD_BOT_TOKEN')
        self.DISCORD_DEFAULT_GUILDS: List[int] = [
            int(guild_id) for guild_id in os.environ.get('DISCORD_DEFAULT_GUILDS', '').split(',') if guild_id
        ] # Split at commas, convert to int, and remove empty strings

        # Rom path Info
        self.POKEMON_RED_PATH = "/EPDCBot/emulation/roms/Pokemon_Red.gb"
        

    @property
    def DATABASE_URI(self):
        """
        Returns the URI for connecting to the PostgreSQL database.
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


def get_logger():
    # Create a logger object.
    logger = logging.getLogger('nextcord')

    # Set the level of this logger. 
    logger.setLevel(logging.INFO)

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



