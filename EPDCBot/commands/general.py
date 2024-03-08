from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import nextcord
import emulation
import random
import requests
from io import BytesIO

class General:
    """
    A class that contains general commands for the bot.

    Attributes:
        bot (commands.Bot): The bot instance.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def echo(self, 
                        interaction: Interaction, 
                        message: str = SlashOption(
                            name="message", 
                            description="The message to send back.", 
                            required=True
                        )
                    ):
            """
            Sends the provided message back as a response.

            Parameters:
            - interaction (Interaction): The interaction object representing the user's interaction with the bot.
            - message (str): The message to send back.

            Returns:
            None
            """
            await interaction.send(message)


    async def show(self, interaction: Interaction):
            """
            Sends an image of Pokemon Red in the interaction channel.

            Parameters:
            - interaction: The interaction object representing the user's interaction with the bot.

            Returns:
            None
            """
            await interaction.response.defer()
            self.bot.log.info("Sending image of Pokemon Red.")
            image = emulation.interact_with_rom(self.bot.config.POKEMON_RED_PATH)
            with BytesIO() as image_binary:
                image.save(image_binary, "PNG")
                image_binary.seek(0)
                await interaction.send("hello", file=nextcord.File(fp=image_binary, filename="pokemon_red.png"))


    # Say Howdy!
    async def hello(self, interaction: Interaction):
        """
        A method that sends a greeting message.

        Parameters:
        - interaction: The interaction object representing the user interaction.

        Returns:
        - None
        """
        await interaction.send("Howdy!")


    # Die Roller
    async def dice(self, interaction: Interaction, 
                        sides: int = SlashOption(
                            name="sides", 
                            description="How many sides do you want?", 
                            required=True,
                            # Adding this eliminates the need for chicken checks.
                            min_value=1,
                            max_value=100
                        )
                    ):
        """
        Roll a dice with the specified number of sides.
        
        Parameters:
        - interaction (Interaction): The interaction object representing the user's command.
        - sides (int): The number of sides on the dice.
        
        Returns:
        None
        """
        await interaction.send(f"d{sides} rolled: {random.randint(1, sides)}.")


    # Cat Fact API interaction
    async def cat_fact(self, interaction: Interaction):
        """
        Retrieves a random cat fact from the CatFact API and sends it as a message.

        Parameters:
        - interaction: The interaction object representing the user's interaction with the bot.

        Returns:
        - None
        """
        # Request JSON from CatFact.
        # Added the APi URL to the config
        response = requests.get(url=self.bot.config.CATFACT_API_URL)
        
        # Parse JSON message.
        data = response.json()
        await interaction.send(data["fact"])


def setup(bot: commands.Bot):
    """
    Sets up the bot by registering slash commands.

    Args:
        bot (commands.Bot): The bot instance.

    Returns:
        None
    """
    # Is this hacky? Yes. Does it work? Also yes.
    # I would KILL to find a cleaner way of doing this...
    # But it's not a priority right now.
    general_slash_commands = General(bot)


    bot.slash_command(
        name="echo",
        description="Sends the same message back.",
        guild_ids=bot.config.DISCORD_DEFAULT_GUILDS
    )(general_slash_commands.echo)
    
    bot.slash_command(
        name="show",
        guild_ids=bot.config.DISCORD_DEFAULT_GUILDS
    )(general_slash_commands.show)

    bot.slash_command(
        name="hello",
        guild_ids=bot.config.DISCORD_DEFAULT_GUILDS
    )(general_slash_commands.hello)

    bot.slash_command(
        name="dice",
        guild_ids=bot.config.DISCORD_DEFAULT_GUILDS
    )(general_slash_commands.dice)

    bot.slash_command(
        name="cat_fact",
        guild_ids=bot.config.DISCORD_DEFAULT_GUILDS
    )(general_slash_commands.cat_fact)