import nextcord
from nextcord.ext import commands
import utils
from database import DatabaseConnection

class EPDCBot(commands.Bot):
    """
    Represents the EPDCBot, a subclass of nextcord.Client.

    Attributes:
        config (utils.Config): The configuration object for the bot.
        log (logging.Logger): The logger object for logging bot events.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, intents=nextcord.Intents.all(), **kwargs)
        self.database = DatabaseConnection()

    async def on_ready(self):
        """
        Event handler called when the bot has successfully connected to Discord.

        This method logs the bot's user information.
        """

        # Setup the Database
        await self.database.setup()

        # Now do a database sweep and make sure everyone in the server is also in the database.
        for guild in self.guilds:
            for member in guild.members:
                async with self.database.get_session() as session:
                    await self.database.get_or_create_member(session, member)

        
        utils.logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        utils.logger.info('------')

        



def main():

    # Set up the logger and config
    bot = EPDCBot()

    # Init Cogs
    bot.load_extensions_from_module('extensions', stop_at_error=True,)

    # Start the bot
    bot.run(utils.Config.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()