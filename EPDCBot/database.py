from sqlalchemy import Column, BigInteger, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
import utils
import nextcord

Base = declarative_base()

engine = create_async_engine(utils.Config.DATABASE_URI(), echo=True, future=True)
SessionLocal: AsyncSession = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


class Member(Base):
    __tablename__ = 'members'

    id = Column(BigInteger(), primary_key=True, autoincrement=False, nullable=False)
    name = Column(String(), nullable=False)
    profile = relationship("Profile", back_populates="member", uselist=False)

class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(BigInteger(), primary_key=True, autoincrement=True, nullable=False)
    member_id = Column(BigInteger(), ForeignKey('members.id'), nullable=False)
    level = Column(BigInteger(), nullable=False)
    experience = Column(BigInteger(), nullable=False)

    member = relationship("Member", back_populates="profile")


async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()

async def convert_nextcord_member(session: Session, member: nextcord.Member) -> Member:
    """
    Converts a Nextcord member to a database member and saves it in the session.

    Args:
        session (Session): The database session.
        member_id (int): The ID of the Nextcord member.
        member_name: The name of the Nextcord member.

    Returns:
        Member: The converted database member.
    """
    db_member = session.get(Member, member.id)
    if db_member is None:
        db_member = Member(id=member.id, name=member.id)
        session.add(db_member)
        await session.commit()
        session.refresh(db_member)
    return db_member

async def add_experience(session: Session, member_id: int, amount: int):
    """
    Add experience points to a member's profile.

    Args:
        session (Session): The database session.
        member_id (int): The ID of the member.
        amount (int): The amount of experience points to add.

    Returns:
        None
    """
    profile = session.query(Profile).filter(Profile.member_id == member_id).first()
    if profile is not None:
        profile.experience += amount
        await session.commit()

async def setup():
    """
    Sets up the database by creating all the tables defined in the metadata.

    This function should be called before any database operations are performed.

    Raises:
        Any exceptions raised by the underlying database engine.

    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def teardown():
    """
    Tear down the database by dropping all tables.

    This function should be called when you want to clean up the database and remove all tables.

    Usage:
        await teardown()

    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)