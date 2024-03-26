from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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