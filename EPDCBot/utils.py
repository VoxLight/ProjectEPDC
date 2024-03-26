import os
import logging
from typing import List

def profile_table_to_next_level(level: int) -> int:
    """
    Returns the experience required to reach the next level.

    args:
        level: int - The current level of the profile.

    returns:
        int - The experience required to reach the next level.
    """
    return round(2**(.9*level))

def profile_table_exp_per_message_by_level(level: int) -> int:
    """
    Returns the experience gained per message based on the level of the profile.

    args:
        level: int - The current level of the profile.

    returns:
        int - The experience gained per message.
    """
    return max(1, round(0.01*profile_table_to_next_level(level)))


class Config:
    """
    Represents the configuration settings for the application.
    """
    # This adjusts several behaviors in the bot. Not suitible for prod when True.
    DEBUG_MODE = True


    LOGGER_NAME = "nextcord"
    LOGGING_DIR = "/logs"
    LOGGING_FILE_NAME = "bot.log"
    LOGGING_LEVEL = logging.INFO

    # The following environment variables are set in a .env file. See .env.example.

    # Database connection information
    DB_USER     = os.environ.get('POSTGRES_USER')
    DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    DB_NAME     = os.environ.get('POSTGRES_DB')
    DB_HOST     = os.environ.get('POSTGRES_HOST')
    DB_PORT     = os.environ.get('POSTGRES_PORT')

    # Discord information
    DISCORD_BOT_TOKEN                 = os.environ.get('DISCORD_BOT_TOKEN')
    DISCORD_DEFAULT_GUILDS: List[int] = [
        int(guild_id) for guild_id in os.environ.get('DISCORD_DEFAULT_GUILDS', '').split(',') if guild_id
    ] # Split at commas, convert to int, and remove empty strings

    # Level Information
    PROFILE_TABLE_STARTING_LEVEL = 1
    PROFILE_TABLE_MAX_LEVEL = 10

    # Rom path Info
    POKEMON_RED_PATH = "/EPDCBot/emulation/roms/Pokemon_Red.gb"
        

    @classmethod
    def DATABASE_URI(cls: "Config"):
        """
        Returns the URI for connecting to the PostgreSQL database.
        """
        return f"postgresql+asyncpg://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
    
    @staticmethod
    def PROFILE_TABLE_TO_NEXT_LEVEL(level: int) -> int:
        """
        Returns the experience required to reach the next level.

        args:
            level: int - The current level of the profile.

        returns:
            int - The experience required to reach the next level.
        """
        return profile_table_to_next_level(level)
    

def get_logger():
    # Create a logger object.
    logger = logging.getLogger(Config.LOGGER_NAME)

    # Set the level of this logger. 
    logger.setLevel(Config.LOGGING_LEVEL)

    # Create the logs directory if it does not exist
    log_dir = os.path.join(os.getcwd(), Config.LOGGING_DIR.strip('/'))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a file handler for outputting log messages to a file
    fh = logging.FileHandler(os.path.join(log_dir, Config.LOGGING_FILE_NAME.strip('/')))

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


logger = get_logger()



