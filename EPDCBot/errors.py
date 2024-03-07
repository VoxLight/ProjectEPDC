from nextcord.ext import commands

class ErrorHandler:

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.on_application_command_error = self.on_application_command_error

    async def on_application_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Command is on cooldown. Try again in {error.retry_after:.2f} seconds.")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("You are missing a required argument.")
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send("You provided a bad argument.")
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send("Command not found.")
        elif isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You do not have permission to use this command.")
        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("An error occurred while executing the command.")
        elif isinstance(error, commands.errors.CommandError):
            await ctx.send("An error occurred while executing the command.")
        else:
            await ctx.send("An unknown error occurred.")

        self.bot.log.error(error.with_traceback(error.__traceback__))