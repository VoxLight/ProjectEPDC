from nextcord.ext import commands
import nextcord
import utils
import exceptions
import aiofiles

class ErrorHandler(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        utils.logger.info("ErrorHandler cog loaded.")

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: commands.Context, error: Exception):

        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Command is on cooldown. Try again in {error.retry_after:.2f} seconds.", ephemeral=True)

        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You are missing a required argument.", ephemeral=True)

        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send("You provided a bad argument.", ephemeral=True)

        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send("Command not found.", ephemeral=True)

        elif isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You do not have permission to use this command.", ephemeral=True)

        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("An error occurred while executing the command.", ephemeral=True)

        elif isinstance(error, commands.errors.CommandError):
            await ctx.send("An error occurred while executing the command.", ephemeral=True)

        # Our errors throw a message we can send in chat.
        elif isinstance(error, exceptions.EPDCBotException):
            await ctx.send(content=str(error), ephemeral=True)

        else:
            await ctx.send("An unknown error occurred.", ephemeral=True)

        utils.logger.error(error.with_traceback(error.__traceback__))

    @commands.is_owner()
    @nextcord.slash_command(name="logs", description="Sends the logs to the user.", guild_ids=utils.Config.DISCORD_DEFAULT_GUILDS, dm_permission=True)
    async def logs(self, interaction: nextcord.Interaction):
        """
        Sends the logs to the user.
        """
        
        # Read the log file asynchronously
        async with aiofiles.open("/app/logs/bot.log", "r") as file:
            logs = await file.readlines()

        # Limit the number of logs to send
        max_logs = 8  # Adjust this number as needed
        logs = logs[:max_logs]

        # Format the logs
        formatted_logs = "\n".join(logs)

        # Send the formatted logs to the user
        await interaction.send(content=f"```\n{formatted_logs}\n```", ephemeral=True)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ErrorHandler(bot))
