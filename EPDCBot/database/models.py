from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Member(Base):
    """
    Represents a member in the database.

    Attributes:
        id (int): The unique identifier for the member.
        discord_id (str): The Discord ID of the member.
        name (str): The name of the member.
        # Add more attributes as needed
    """
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    # Add more columns as needed

class Guild(Base):
    """
    Represents a guild in the application.

    Attributes:
        id (int): The unique identifier for the guild.
        guild_id (str): The unique identifier for the guild in the external service.
        name (str): The name of the guild.
        # Add more attributes as needed
    """
    __tablename__ = 'guilds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    # Add more columns as needed


def init_tables(engine):
    Base.metadata.create_all(engine)

