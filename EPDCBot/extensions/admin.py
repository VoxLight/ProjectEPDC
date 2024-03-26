import nextcord
from nextcord.ext import commands
from nextcord.ext import application_checks

import os
import time
import tempfile
from typing import List

import asyncio
import asyncio.subprocess as asyncprocess

import utils
import database

async def run_local_command(command: str, *args: List[str]) -> str | None:
    """
    Executes a local command and returns the output.
    Equivelant to Popen([command, *args], ... ).

    Args:
        command (str): The command to be executed.
        args (List[str]): Additional arguments for the command.

    Returns:
        str | None: The output of the command if successful, None otherwise.
    """

    process = await asyncio.create_subprocess_exec(command, *args, stdout=asyncprocess.PIPE, stderr=asyncprocess.PIPE, cwd=os.getcwd())

    # Poll for process completion in an async manner
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        utils.logger.error(f"Error running command: {command} {' '.join(args)}")
        utils.logger.error(stderr.decode("utf-8"))
        return stderr.decode("utf-8")
    
    return stdout.decode("utf-8")

class ShellSession:
    def __init__(self):
        self.process = None

    @property
    def is_running(self):
        return self.process is not None

    async def start(self):
        self.process = await asyncio.create_subprocess_shell(
            "/bin/bash",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

    async def run_command(self, command):
        if not self.is_running:
            await self.start()

        self.process.stdin.write((command + "\n").encode())
        await self.process.stdin.drain()

        output = []
        while True:
            try:
                line = await asyncio.wait_for(self.process.stdout.readline(), timeout=1.0)
            except asyncio.TimeoutError:
                break  # assume the command has finished if readline times out

            if not line:  # EOF
                break
            output.append(line.decode().strip())

        return "\n".join(output)

    async def stop(self):
        if self.process:
            self.process.terminate()
            await self.process.wait()


class AdminCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.shell = ShellSession()

        utils.logger.info("AdminCommands cog loaded.")


    @application_checks.is_owner()
    @nextcord.slash_command(name="reload", description="Reloads all the cogs.", guild_ids=utils.Config.DISCORD_DEFAULT_GUILDS)
    async def reload(self, interaction: nextcord.Interaction) -> None:
        """
        Reloads all the cogs.
        """
        for extension in list(self.bot.extensions):
            self.bot.reload_extension(extension)
        await interaction.send("Reloaded all cogs.", ephemeral=True)


    @application_checks.is_owner()
    @nextcord.message_command(name="exec", guild_ids=utils.Config.DISCORD_DEFAULT_GUILDS)
    async def exec(self, interaction: nextcord.Interaction, message: nextcord.Message) -> None:
        """
            Find the code inside a python code block in discord and execute it. 
            fmt: 
                ```Python
                    <code>
                ```
        """
        # Is there a better way to do this? The question I am ALWAYS asking myself...
        msg = message.content
        code = None

        # Error handling
        if msg.startswith("```Python") and msg.endswith("```"):
            code = msg[9:-3]
        else:
            await interaction.send("No code block found in the message.")
            return
        
        if code == None:
            await interaction.send("No code found in the message.")
            return
        
        # Create a temp file to store and pass to the command.
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp:
            temp.write(code)
            temp_path = temp.name

        # Run the command and time it.
        start = time.perf_counter()
        output = await run_local_command("python3", temp_path)
        end = time.perf_counter()

        # Meta info appended to the end.
        meta_msg = f"\n# Execution took {end-start:.2f} seconds."
        msg = f"```Bash\n{output}\n{meta_msg}\n```"
        os.remove(temp_path)
        await message.reply(content=msg)
        await interaction.send("Executed the code.", ephemeral=True)


    @application_checks.is_owner()
    @nextcord.message_command(name="pgexec", guild_ids=utils.Config.DISCORD_DEFAULT_GUILDS)
    async def pgexec_message(self, interaction: nextcord.Interaction, message: nextcord.Message) -> None:
        """
        Find the SQL query inside a postgres code block in discord and execute it. 
        fmt: 
            ```postgres
                <query>
            ```
        """
        msg = message.content
        query = None

        # Error handling
        if msg.startswith("```postgres") and msg.endswith("```"):
            query = msg[11:-3]
        else:
            await interaction.send("No code block found in the message.")
            return
        
        if query == None:
            await interaction.send("No query found in the message.")
            return

        # Execute the query and format the result
        result = await database.DatabaseManager.active_db.execute_query(query)
        if result.returns_rows:
            rows = result.all()
            output = '\n'.join(map(str, rows))
            await interaction.send(f"```postgres\n{output or 'This Table is Empty...'}\n```")
            await interaction.delete_original_message(delay=30)
        else:
            await interaction.send("Query returned no rows, but it did execute successfully.")
            await interaction.delete_original_message(delay=3)

    @application_checks.is_owner()
    @nextcord.slash_command(name="pgexec", description="Executes a PostgreSQL query.", guild_ids=utils.Config.DISCORD_DEFAULT_GUILDS)
    async def pgexec(self, interaction: nextcord.Interaction, query: str, hidden: bool = True) -> None:
        """
        Sends a PostgreSQL query to the database.
        """
        result = await database.DatabaseManager.active_db.execute_query(query)
        rows = result.all()
        output = '\n'.join(map(str, rows))
        await interaction.send(f"```postgres\n{output or 'No Output.'}\n```", ephemeral=hidden)


    @application_checks.is_owner()
    @nextcord.slash_command(name="fsexec", description="Executes a bash command in the terminal.", guild_ids=utils.Config.DISCORD_DEFAULT_GUILDS)
    async def fsexec(self, interaction: nextcord.Interaction, command: str, hidden: bool = True) -> None:
        """
        Sends a command to the terminal and returns the stdout.
        """

        # Sometimes the bot just hangs and doesn't respond to the command.
        await interaction.response.defer(ephemeral=hidden, )
        if not self.shell.process or self.shell.process.returncode is not None:
            await self.shell.start()

        output = await self.shell.run_command(command)

        msg = f"```Python\n{self.bot.user.name}:{os.getcwd()}$ {command}\n{output}\n```"
        await interaction.followup.send(content=msg, ephemeral=hidden)


def setup(bot: commands.Bot):
    if utils.Config.DEBUG_MODE:
        bot.add_cog(AdminCommands(bot))
        

    