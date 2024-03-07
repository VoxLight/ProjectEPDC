from nextcord import SlashApplicationCommand, Interaction, SlashOption
from nextcord.ext import commands
import nextcord
import emulation
import random
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

    async def hello(self, interaction: Interaction):
        say_hi: str = "Howdy!"
        await interaction.send(say_hi)

    async def dice(self,
                   interaction: Interaction,
                   sides: int = SlashOption(
                        name="sides", 
                        description="How many sides do you want?", 
                        required=True
                    )
                ):
        returnMessage: str = ""
        if(sides>0):
            roll: int = random.randint(a=1, b=sides)
            returnMessage = f"d{sides} rolled: {roll}."
        else:
            returnMessage = "Invalid number of sides."

        await interaction.send(returnMessage)

                
         

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