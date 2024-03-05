from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    # Add more columns as needed

class Guild(Base):
    __tablename__ = 'guilds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    # Add more columns as needed


def init_tables(engine):
    Base.metadata.create_all(engine)

