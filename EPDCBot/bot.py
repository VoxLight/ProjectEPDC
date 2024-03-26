import nextcord
from nextcord.ext import commands
import utils
import os
import database

class EPDCBot(commands.Bot):
    """
    Represents the EPDCBot, a subclass of nextcord.Client.

    Attributes:
        config (utils.Config): The configuration object for the bot.
        log (logging.Logger): The logger object for logging bot events.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, intents=nextcord.Intents.all(), **kwargs)
        self.db_manager = database.DatabaseManager()

    async def on_ready(self):
        """
        Event handler called when the bot has successfully connected to Discord.

        This method logs the bot's user information.
        """

        # Setup the Database
        await database.setup()

        # Now do a database sweep and make sure everyone in the server is also in the database.
        for guild in self.guilds:
            for member in guild.members:
                session: database.AsyncSession = await database.get_session()
                await database.get_or_create_member(session, member.id, member.name)
                await session.commit()
                await session.close()

        
        utils.logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        utils.logger.info('------')

    def load_cogs_from_directory(self, directory: str):
        """
        Loads all cogs from a directory.

        Args:
            directory (str): The directory to load cogs from.
        """
        for filename in os.listdir(directory):
            # ignore hidden files and non-python files
            if not filename.startswith("_") and filename.endswith('.py'):
                self.load_extension(f'{directory}.{filename[:-3]}')
        



def main():

    # Set up the logger and config
    bot = EPDCBot()

    # Init Cogs
    bot.load_cogs_from_directory('extensions')

    # Start the bot
    bot.run(utils.Config.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()