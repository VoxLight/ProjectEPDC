import sqlalchemy
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm.session
import utils
from .models import init_tables
import exceptions


class Database:
    """
    Represents a connection to a PostgreSQL database using SQLAlchemy.
    """

    _CURRENTLY_BOUND = False

    def __init__(self, config: utils.Config, bind_on_init: bool = True):
        """
        Initializes a new instance of the Database class.

        Args:
            config (utils.Config): The configuration object containing the database URI.
            bind_on_init (bool, optional): Whether to bind the database engine on initialization. Defaults to True.
        
        Raises:
            exceptions.DatabaseException: If a Database Engine has already been bound and `bind_on_init` is True.
        """
        self.config = config
        self.engine = self.create_engine()
        if bind_on_init and not Database._CURRENTLY_BOUND:
            init_tables(self.engine)
            Database._CURRENTLY_BOUND = True
        elif bind_on_init and Database._CURRENTLY_BOUND:
            raise exceptions.DatabaseException("A Database Engine has already been bound. Database is a Singleton.")
        self.session = self.create_session(self.engine)

    def create_engine(self) -> sqlalchemy.engine.Engine:
        """
        Creates and returns a SQLAlchemy engine object for connecting to a PostgreSQL database.
        
        Returns:
            sqlalchemy.engine.Engine: The SQLAlchemy engine object.
        """
        return sqlalchemy.create_engine(self.config.DATABASE_URI, echo=True)
    
    def create_session(self, engine) -> sqlalchemy.orm.session.Session:
        """
        Creates and returns a SQLAlchemy session object for interacting with the database.
        
        Args:
            engine (sqlalchemy.engine.Engine): The SQLAlchemy engine object.
        
        Returns:
            sqlalchemy.orm.session.Session: The SQLAlchemy session object.
        """
        _Session = sessionmaker(bind=engine)
        return _Session()

