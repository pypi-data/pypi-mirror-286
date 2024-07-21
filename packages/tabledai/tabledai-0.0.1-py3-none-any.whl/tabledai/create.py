import hashlib, os, logging
import pandas as pd
from sqlalchemy import create_engine, exc, text, Column, MetaData, Table as SQLTable, types
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(message)s')
load_dotenv(override=True)

class PostgresDB:
    def __init__(self, name: str = 'db', postgres_password: str = None, postgres_host: str = None) -> None:
        self.name = name
        self.postgres_password = postgres_password or os.getenv("POSTGRES_DB_PASSWORD")
        self.postgres_host = postgres_host or os.getenv("POSTGRES_DB_HOST")

        if not self.postgres_password or not self.postgres_host:
            raise ValueError("Please provide a password and host for the database either by passing them in or providing them in a .env file.")

        self.engine = create_engine(f'postgresql://postgres:{self.postgres_password}@{self.postgres_host}/{self.name}')
        logging.info(f"Connecting to database '{self.name}'...")
        logging.info(f"-"*75)
        try:
            self.connection = self.engine.connect()
        except exc.OperationalError as e:
            if 'does not exist' in str(e):
                logging.info(f"Database '{self.name}' does not exist.")
                logging.info(f"-"*75)
                self._create_database(self.name)
                self.engine = create_engine(f'postgresql://postgres:{self.postgres_password}@{self.postgres_host}/{self.name}')
                self.connection = self.engine.connect()

    def _create_database(self, db_name: str) -> None:
        logging.info(f"Creating database '{db_name}'...")
        logging.info(f"-"*75)
        engine = create_engine(f'postgresql://postgres:{self.postgres_password}@{self.postgres_host}/postgres')
        conn = engine.connect().execution_options(isolation_level="AUTOCOMMIT")
        
        try:
            conn.execute(text(f"CREATE DATABASE {db_name}"))
            logging.info(f"Database '{db_name}' created successfully.")
            logging.info(f"-"*75)
        except exc.ProgrammingError as e:
            logging.error(f"ProgrammingError: {e}")
            if 'already exists' in str(e):
                logging.info(f"Database '{db_name}' already exists.")
                logging.info(f"-"*75)
            else:
                raise
        finally:
            conn.close()

    def create_tables(self, data_directory: str) -> None:
        for file_name in os.listdir(data_directory):
            if file_name.endswith('.csv') or file_name.endswith('.xlsx'):
                table_name = os.path.splitext(file_name)[0]
                file_path = os.path.join(data_directory, file_name)
                logging.info(f"Creating or updating table '{table_name}' from file '{file_name}'...")
                logging.info(f"-"*75)
                Table(self, table_name, file_path)
            else:
                logging.info(f"Skipping file '{file_name}' as it is not a CSV or Excel file.")
                logging.info(f"-"*75)

    def delete_tables(self, tables: list = [], all: bool = False, confirm: bool = True) -> None:
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        tables = tables if not all else [table for table in metadata.tables.keys()]

        def _delete_table(connection, table):
            try:
                table = metadata.tables[table]
                logging.info(f"Dropping table '{table}'...")
                logging.info(f"-"*75)
                table.drop(connection)
                logging.info(f"Table {table} dropped successfully.")
                logging.info(f"-"*75)
            except Exception as e:
                logging.error(f"Error deleting table {table}: {e}")
                logging.info(f"-"*75)

        with self.engine.begin() as connection:
            for table in tables:
                if confirm:
                    print("\n")
                    print("*"*100)
                    response = input(f"Are you sure you want to delete table '{table}'? This action can't be undone. (y/n): ")
                    print("*"*100,"\n")
                    logging.info(f"-"*75)
                    if response.lower().strip() == 'y':
                        _delete_table(connection, table)
                    else:
                        logging.info(f"Table '{table}' deletion aborted.")
                        logging.info(f"-"*75)
                else:
                    _delete_table(connection, table)

    def delete(self, confirm: bool = True) -> None:
        engine = create_engine(f'postgresql://postgres:{self.postgres_password}@{self.postgres_host}/postgres')
        conn = engine.connect().execution_options(isolation_level="AUTOCOMMIT")
        
        def _delete_db():
            try:
                conn.execute(text(f"""
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = '{self.name}' AND pid <> pg_backend_pid();
                """))
                conn.execute(text(f"DROP DATABASE {self.name}"))
                logging.info(f"Database '{self.name}' deleted successfully.")
                logging.info(f"-"*75)
            except exc.ProgrammingError as e:
                logging.error(f"ProgrammingError: {e}")
                if 'does not exist' in str(e):
                    logging.info(f"Database '{self.name}' does not exist.")
                    logging.info(f"-"*75)
                else:
                    raise
            finally:
                conn.close()
            
        if confirm:
            print("\n")
            print("*"*100)
            response = input(f"Are you sure you want to delete database '{self.name}'? This action can't be undone. (y/n): ")
            print("*"*100,"\n")
            logging.info(f"-"*75)
            if response.lower().strip() != 'y':
                logging.info(f"Database '{self.name}' deletion aborted.")
                logging.info(f"-"*75)
                return
            else:
                _delete_db()
        else:
            _delete_db()

class Table:
    def __init__(self, db: PostgresDB, table_name: str, file_path: str = None) -> None:
        self.db = db
        self.table_name = table_name
        if file_path:
            self.file_path = file_path
            self.table = self._define_table()
            self._load_csv_to_table()

    def _define_table(self) -> SQLTable:
        data = pd.read_csv(self.file_path)
        metadata = MetaData()
        columns = [Column(column_name, self._map_types(dtype)) for column_name, dtype in data.dtypes.items()]
        return SQLTable(self.table_name, metadata, *columns)

    def _load_csv_to_table(self) -> None:
        data = pd.read_csv(self.file_path)
        self.table.metadata.create_all(self.db.engine)

        with self.db.engine.connect() as connection:
            try:
                existing_data = pd.read_sql_table(self.table_name, connection)
            except Exception as e:
                logging.error(f"Error reading existing data: {e}")
                logging.info(f"-"*75)
                existing_data = pd.DataFrame()

        existing_data['_hash'] = existing_data.apply(lambda row: hashlib.md5(pd.util.hash_pandas_object(row, index=True).values).hexdigest(), axis=1)
        data['_hash'] = data.apply(lambda row: hashlib.md5(pd.util.hash_pandas_object(row, index=True).values).hexdigest(), axis=1)

        non_duplicate_data = data[~data['_hash'].isin(existing_data['_hash'])].drop(columns=['_hash'])

        if not non_duplicate_data.empty:
            with self.db.engine.connect() as connection:
                try:
                    non_duplicate_data.to_sql(self.table_name, connection, if_exists='append', index=False)
                    logging.info(f"New data has been successfully inserted for table '{self.table_name}'.")
                    logging.info(f"-"*75)
                except Exception as e:
                    logging.error(f"Error inserting non-duplicate data for table {self.table_name}: {e}")
                    logging.info(f"-"*75)
        else:
            logging.info(f"No new data to insert for table '{self.table_name}'. All records are duplicates.")
            logging.info(f"-"*75)
    
    def _map_types(self, dtype: pd.api.types) -> types.TypeEngine:
        if pd.api.types.is_integer_dtype(dtype):
            return types.Integer()
        elif pd.api.types.is_float_dtype(dtype):
            return types.Float()
        elif pd.api.types.is_bool_dtype(dtype):
            return types.Boolean()
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            return types.DateTime()
        else:
            return types.String()

