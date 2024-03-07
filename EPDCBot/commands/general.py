from nextcord import SlashApplicationCommand, Interaction, SlashOption
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
            await interaction.send(message)

    async def show(self, interaction: Interaction):
        await interaction.response.defer()
        self.bot.log.info("Sending image of Pokemon Red.")
        image = emulation.interact_with_rom(self.bot.config.POKEMON_RED_PATH)
        with BytesIO() as image_binary:
            image.save(image_binary, "PNG")
            image_binary.seek(0)
            await interaction.send("hello", file=nextcord.File(fp=image_binary, filename="pokemon_red.png"))

    # Say Howdy!
    async def hello(self, interaction: Interaction):
        say_hi: str = "Howdy!"
        await interaction.send(say_hi)

    # Die Roller
    async def dice(self,
                   interaction: Interaction,
                   sides: int = SlashOption(
                        name="sides", 
                        description="How many sides do you want?", 
                        required=True
                    )
                ):
        return_message: str = ""
        if(sides>0):
            roll: int = random.randint(a=1, b=sides)
            return_message = f"d{sides} rolled: {roll}."
            if(roll==sides):
                return_message += f"\nMax roll! Nice!"
        else:
            return_message = "Invalid number of sides."

        await interaction.send(return_message)

    # Cat Fact API interaction
    async def cat_fact(self, interaction: Interaction):
        # Request JSON from CatFact.
        url_catfact: str = "https://catfact.ninja/fact"
        response = requests.get(url=url_catfact)

        # Parse JSON message.
        API_data = response.json()
        json_catfact_fact: str = "fact" # json fact definition
        catfact: str = API_data[json_catfact_fact] # catfact from json parse
        await interaction.send(catfact)


def setup(bot: commands.Bot):
    """
    Sets up the bot by registering slash commands.

    Args:
        bot (nxtcmd.Bot): The bot instance.

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