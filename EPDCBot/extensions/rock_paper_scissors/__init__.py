from .rock_paper_scissors import RockPaperScissors
from .cog import RockPaperScissorsCog



def setup(bot: commands.Bot) -> None:
    bot.add_cog(RockPaperScissorsCommands(bot))