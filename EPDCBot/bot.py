import nextcord
from nextcord.ext import commands as nextcord_commands
import utils
import logging
import commands

class EPDCBot(nextcord_commands.Bot):
    """
    Represents the EPDCBot, a subclass of nextcord.Client.

    Attributes:
        config (utils.Config): The configuration object for the bot.
        log (logging.Logger): The logger object for logging bot events.
    """

    def __init__(self, config: utils.Config, log: logging.Logger):
        super().__init__(intents=nextcord.Intents.all())  # Set up intents

        self.config: utils.Config = config
        self.log: logging.Logger = log

    async def on_ready(self):
        """
        Event handler called when the bot has successfully connected to Discord.

        This method logs the bot's user information.
        """
        self.log.info(f'Logged in as {self.user} (ID: {self.user.id})')
        self.log.info('------')
        



def main():

    # Set up the logger and config
    log    = utils.get_logger()
    config = utils.Config()
    bot    = EPDCBot(config, log)

    # Init commands
    commands.general.setup(bot)

    # Start the bot
    bot.run(config.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()