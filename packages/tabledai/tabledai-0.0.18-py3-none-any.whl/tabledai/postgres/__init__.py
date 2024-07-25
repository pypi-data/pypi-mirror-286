import os, logging
from sqlalchemy import create_engine, MetaData, exc
from .database_management import DatabaseManagement
from .llm_integration import LLMIntegration
from .query_handling import QueryHandling
from dotenv import load_dotenv

load_dotenv(override=True)
logging.basicConfig(level=logging.INFO, format='%(message)s')

class PostgresDB(DatabaseManagement, LLMIntegration, QueryHandling):
    def __init__(self, name: str = 'db', postgres_username: str = None, postgres_password: str = None, postgres_host: str = None) -> None:
        self.name = name
        self.postgres_username = postgres_username or os.getenv("POSTGRES_DB_USERNAME")
        self.postgres_password = postgres_password or os.getenv("POSTGRES_DB_PASSWORD")
        self.postgres_host = postgres_host or os.getenv("POSTGRES_DB_HOST")
        if not self.postgres_password or not self.postgres_host:
            raise ValueError("Please provide a password and host for the database either by passing them in or providing them in a .env file.")

        self.default_engine = create_engine(f'postgresql://{self.postgres_username}:{self.postgres_password}@{self.postgres_host}/postgres')
        logging.info(f"Connecting to the default 'postgres' database...")
        self._ensure_database_exists()
        self.engine = create_engine(f'postgresql://{self.postgres_username}:{self.postgres_password}@{self.postgres_host}/{self.name}')
        self.metadata = MetaData()
        logging.info(f"Connecting to database '{self.name}'...")
        self.connection = self._connect_to_database()

    def _ensure_database_exists(self):
        try:
            self.default_engine.connect()
            logging.info("Successfully connected to the default 'postgres' database.")
            self._create_database(db_name=self.name)
        except exc.OperationalError as e:
            logging.error(f"Failed to connect to the default 'postgres' database: {e}")
            raise

    def _connect_to_database(self):
        try:
            connection = self.engine.connect()
            logging.info("Successfully connected to the database.")
            return connection
        except exc.OperationalError as e:
            logging.error(f"Failed to connect to the database '{self.name}': {e}")
            raise