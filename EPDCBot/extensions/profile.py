from nextcord.ext import commands
import nextcord
import utils
import database


class ProfileCommands(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        utils.logger.info("Profile cog loaded.")


    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author == self.bot.user:
            return

        session = await database.get_session()
        profile = await database.get_or_create_member(
            session, message.author
        ).profile
        await database.add_experience(
            session, message.author.id, 
            utils.profile_table_exp_per_message_by_level
        )
        




def setup(bot: commands.Bot) -> None:
    bot.add_cog(ProfileCommands(bot))
