from sqlalchemy import create_engine ##replaced to sqlalchemy because more modern and no warnings from VScode
import pandas as pd

class PostgresConnectorContextManager:
    def __init__(self, db_host: str, db_name: str, db_user: str, db_password: str, db_port: int = 5432):
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port
        self.engine = None

    def __enter__(self):
        try:
            conn_str = (
                f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
            self.engine = create_engine(conn_str)
            return self
        except Exception as e:
            raise RuntimeError(f"Failed to connect to PostgreSQL via SQLAlchemy: {e}")

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.engine:
            self.engine.dispose()

    def get_data_sql(self, sql):
        if self.engine is None:
            raise RuntimeError("Connection is not established.")
        try:
            df = pd.read_sql_query(sql, self.engine)
            return df
        except Exception as e:
            raise RuntimeError(f"Failed to execute query: {e}")