import hashlib
import logging
import warnings
import os
import re
import pandas as pd
from sqlalchemy import create_engine, exc, text, Column, MetaData, Table as SQLTable
import chardet
from .utils import disable_logging, map_types

class DatabaseManagement:
    def _create_database(self, db_name: str) -> None:
        engine = create_engine(f'postgresql://{self.postgres_username}:{self.postgres_password}@{self.postgres_host}/postgres')
        conn = engine.connect().execution_options(isolation_level="AUTOCOMMIT")
        try:
            conn.execute(text(f"CREATE DATABASE {db_name}"))
            logging.info(f"Database '{db_name}' created successfully.")
        except exc.ProgrammingError as e:
            if 'already exists' in str(e):
                logging.info(f"Database '{db_name}' already exists.")
            else:
                raise
        except exc.OperationalError:
            logging.error("The 'postgres' database does not exist. Please create it or use another default database.")
            raise
        finally:
            conn.close()

    def create_tables(self, data_directory: str) -> None:
        for file_name in os.listdir(data_directory):
            if file_name.endswith('.csv') or file_name.endswith('.xlsx'):
                table_name = os.path.splitext(file_name)[0]
                file_path = os.path.join(data_directory, file_name)
                logging.info(f"Creating or updating table '{table_name}' from file '{file_name}'...")
                self._create_or_update_table(table_name, file_path)

    def _create_or_update_table(self, table_name: str, file_path: str) -> None:
        @disable_logging
        def _clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
            df.columns = [
                re.sub(r'[^a-z0-9_]', '', col.replace('%', '_percent').replace('+', '_plus').replace('-', '_minus').replace('/', '_per_').strip().lower().replace(' ', '_'))
                for col in df.columns
            ]
            return df
        
        @disable_logging
        def _convert_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
            def _is_datetime_column(column):
                if column.dtype != object:
                    return False
                date_patterns = [
                    r'\d{2}/\d{2}/\d{4}',
                    r'\d{4}/\d{2}/\d{2}',
                    r'\d{2}-\d{2}-\d{4}',
                    r'\d{4}-\d{2}-\d{2}',
                    r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}',
                    r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}',
                    r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}',
                    r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
                ]
                for pattern in date_patterns:
                    if column.str.match(pattern).any():
                        try:
                            with warnings.catch_warnings():
                                warnings.simplefilter("ignore", UserWarning)
                                pd.to_datetime(column, errors='raise', dayfirst=True)
                            return True
                        except (ValueError, TypeError):
                            continue
                return False

            datetime_columns = [col for col in df.columns if _is_datetime_column(df[col])]
            for column in datetime_columns:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    df[column] = pd.to_datetime(df[column], dayfirst=True).dt.strftime('%Y-%m-%d %H:%M:%S')
            return df

        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        data = pd.read_csv(file_path, encoding=encoding)
        data = _clean_column_names(data)
        data = _convert_datetime_columns(data)

        metadata = MetaData()
        columns = [Column(column_name, map_types(dtype)) for column_name, dtype in data.dtypes.items()]
        table = SQLTable(table_name, metadata, *columns)
        table.metadata.create_all(self.engine)

        with self.engine.connect() as connection:
            try:
                existing_data = pd.read_sql_table(table_name, connection)
            except Exception:
                existing_data = pd.DataFrame()

        existing_data['_hash'] = existing_data.apply(lambda row: hashlib.md5(pd.util.hash_pandas_object(row, index=True).values).hexdigest(), axis=1)
        data['_hash'] = data.apply(lambda row: hashlib.md5(pd.util.hash_pandas_object(row, index=True).values).hexdigest(), axis=1)

        non_duplicate_data = data[~data['_hash'].isin(existing_data['_hash'])].drop(columns=['_hash'])

        if not non_duplicate_data.empty:
            with self.engine.connect() as connection:
                try:
                    non_duplicate_data.to_sql(table_name, connection, if_exists='append', index=False)
                    logging.info(f"New data has been successfully inserted for table '{table_name}'.")
                except Exception as e:
                    logging.error(f"Error inserting non-duplicate data for table {table_name}: {e}")

    def delete_tables(self, tables: list = [], all: bool = False, confirm: bool = True) -> None:
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        tables = tables if not all else list(metadata.tables.keys())

        def _delete_table(connection, table):
            try:
                table = metadata.tables[table]
                logging.info(f"Dropping table '{table}'...")
                table.drop(connection)
                logging.info(f"Table {table} dropped successfully.")
            except Exception as e:
                logging.error(f"Error deleting table {table}: {e}")

        with self.engine.begin() as connection:
            for table in tables:
                if confirm:
                    response = input(f"Are you sure you want to delete table '{table}'? This action can't be undone. (y/n): ")
                    if response.lower().strip() == 'y':
                        _delete_table(connection, table)
                    else:
                        logging.info(f"Table '{table}' deletion aborted.")
                else:
                    _delete_table(connection, table)

    def delete(self, confirm: bool = True) -> None:
        engine = create_engine(f'postgresql://{self.postgres_username}:{self.postgres_password}@{self.postgres_host}/postgres')
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
            except exc.ProgrammingError as e:
                if 'does not exist' in str(e):
                    logging.info(f"Database '{self.name}' does not exist.")
                else:
                    raise
            except exc.OperationalError:
                logging.error("The 'postgres' database does not exist. Please create it or use another default database.")
                raise
            finally:
                conn.close()

        if confirm:
            response = input(f"Are you sure you want to delete database '{self.name}'? This action can't be undone. (y/n): ")
            if response.lower().strip() == 'y':
                _delete_db()
            else:
                logging.info(f"Database '{self.name}' deletion aborted.")
        else:
            _delete_db()

    def check_primary_key(self, table_name: str) -> None:
        with self.engine.connect() as con:
            result = con.execute(text(f"""
                SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_name = '{table_name}' AND tc.constraint_type = 'PRIMARY KEY';
            """))
            primary_keys = result.fetchall()
            result_dict = {'exists': len(primary_keys) > 0, 'field': primary_keys[0][0] if primary_keys else None}
            logging.info(f"Primary key check for table '{table_name}': {result_dict}")

    def add_primary_key(self, table_name: str, field: str) -> None:
        with self.engine.connect() as con:
            try:
                result = con.execute(text(f"""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.table_name = '{table_name}' AND tc.constraint_type = 'PRIMARY KEY';
                """))
                existing_primary_keys = [row[0] for row in result.fetchall()]

                if len(existing_primary_keys) == 1 and existing_primary_keys[0] == field:
                    return

                fk_constraints = []

                for existing_pk in existing_primary_keys:
                    fk_result = con.execute(text(f"""
                        SELECT tc.table_name, kcu.column_name, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name, tc.constraint_name
                        FROM information_schema.table_constraints AS tc 
                        JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                        WHERE tc.constraint_type = 'FOREIGN KEY' AND ccu.table_name='{table_name}' AND ccu.column_name='{existing_pk}';
                    """))
                    fk_constraints = fk_result.fetchall()

                    for fk in fk_constraints:
                        fk_constraint_name = fk[4]
                        fk_table_name = fk[0]
                        con.execute(text(f"""
                            ALTER TABLE {fk_table_name} DROP CONSTRAINT {fk_constraint_name};
                        """))
                        logging.info(f"Dropped foreign key constraint '{fk_constraint_name}' from table '{fk_table_name}'.")

                    con.execute(text(f"""
                        ALTER TABLE {table_name} DROP CONSTRAINT {existing_pk};
                    """))
                    logging.info(f"Dropped existing primary key constraint '{existing_pk}' from table '{table_name}'.")

                con.execute(text(f"""
                    ALTER TABLE {table_name}
                    ADD PRIMARY KEY ({field});
                """))
                logging.info(f"Primary key '{field}' added to table '{table_name}'.")

                for fk in fk_constraints:
                    fk_constraint_name = fk[4]
                    fk_table_name = fk[0]
                    fk_column_name = fk[1]
                    foreign_table_name = fk[2]
                    foreign_column_name = fk[3]
                    con.execute(text(f"""
                        ALTER TABLE {fk_table_name}
                        ADD CONSTRAINT {fk_constraint_name}
                        FOREIGN KEY ({fk_column_name})
                        REFERENCES {foreign_table_name} ({foreign_column_name});
                    """))
                    logging.info(f"Recreated foreign key constraint '{fk_constraint_name}' on table '{fk_table_name}'.")
                con.commit()
            except Exception as e:
                logging.error(f"Failed to update primary key '{field}' for table '{table_name}': {e}")

    def drop_primary_key(self, table_name: str) -> None:
        with self.engine.connect() as con:
            try:
                result = con.execute(text(f"""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.table_name = '{table_name}' AND tc.constraint_type = 'PRIMARY KEY';
                """))
                existing_primary_keys = [row[0] for row in result.fetchall()]

                for existing_pk in existing_primary_keys:
                    con.execute(text(f"""
                        ALTER TABLE {table_name} DROP CONSTRAINT {existing_pk};
                    """))
                    logging.info(f"Dropped existing primary key constraint '{existing_pk}' from table '{table_name}'.")
            except Exception as e:
                logging.error(f"Failed to drop primary key constraints from table '{table_name}': {e}")

    def check_foreign_keys(self, table_name: str) -> bool:
        with self.engine.connect() as con:
            result = con.execute(text(f"""
                SELECT tc.constraint_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_name = '{table_name}' AND tc.constraint_type = 'FOREIGN KEY';
            """))
            foreign_keys = result.fetchall()
            result_dict = {'exists': len(foreign_keys) > 0, 'constraints': [fk[0] for fk in foreign_keys]}
            logging.info(f"Foreign key check for table '{table_name}': {result_dict}")
            return result_dict

    def add_foreign_key(self, table_name: str, field: str, reference_table: str, reference_field: str) -> None:
        with self.engine.connect() as con:
            try:
                self.add_primary_key(reference_table, reference_field)

                result = con.execute(text(f"""
                    SELECT tc.constraint_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.table_name = '{table_name}' AND tc.constraint_type = 'FOREIGN KEY' AND kcu.column_name = '{field}';
                """))
                existing_constraints = result.fetchall()

                for constraint in existing_constraints:
                    constraint_name = constraint[0]
                    con.execute(text(f"""
                        ALTER TABLE {table_name} DROP CONSTRAINT {constraint_name};
                    """))
                    logging.info(f"Dropped existing foreign key constraint '{constraint_name}' from table '{table_name}'.")

                con.execute(text(f"""
                    ALTER TABLE {table_name}
                    ADD CONSTRAINT fk_{table_name}_{field}
                    FOREIGN KEY ({field})
                    REFERENCES {reference_table} ({reference_field});
                """))
                con.commit()
                logging.info(f"Foreign key '{field}' added to table '{table_name}' referencing '{reference_table}({reference_field})'.")
            except Exception as e:
                logging.error(f"Failed to update foreign key '{field}' for table '{table_name}': {e}")

    def drop_foreign_key(self, table_name: str, field: str = None, all: bool = False) -> None:
        if not field and not all:
            logging.error("Please provide a field or set 'all' to True to drop all foreign key constraints.")
            return
        with self.engine.begin() as connection:
            try:
                if all:
                    result = connection.execute(text(f"""
                        SELECT tc.constraint_name
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name = kcu.constraint_name
                        WHERE tc.table_name = '{table_name}' AND tc.constraint_type = 'FOREIGN KEY';
                    """))
                    foreign_keys = result.fetchall()
                    for fk in foreign_keys:
                        connection.execute(text(f"ALTER TABLE {table_name} DROP CONSTRAINT {fk[0]}"))
                        logging.info(f"Dropped foreign key constraint '{fk[0]}' from table '{table_name}'.")
                else:
                    result = connection.execute(text(f"""
                        SELECT tc.constraint_name
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name = kcu.constraint_name
                        WHERE tc.table_name = '{table_name}' AND tc.constraint_type = 'FOREIGN KEY' AND kcu.column_name = '{field}';
                    """))
                    foreign_keys = result.fetchall()
                    for fk in foreign_keys:
                        connection.execute(text(f"ALTER TABLE {table_name} DROP CONSTRAINT {fk[0]}"))
                        logging.info(f"Dropped foreign key constraint '{fk[0]}' from table '{table_name}'.")

            except Exception as e:
                logging.error(f"Failed to drop foreign key constraints from table '{table_name}': {e}")

    def _query_db(self, sql: str) -> dict:
        with self.engine.connect() as con:
            try:
                result = con.execute(text(sql))
                data = result.fetchall()
                columns = result.keys()
                df = pd.DataFrame(data, columns=columns)
                return {'success': True, 'data': df}
            except Exception as e:
                # logging.error(f"""Error querying the database: {e}""")
                return {'success': False, 'data': str(e)}
