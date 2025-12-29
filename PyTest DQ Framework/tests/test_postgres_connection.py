from src.connectors.postgres.postgres_connector import PostgresConnectorContextManager
import os


def test_postgres_connection():
    db_host = os.environ.get("DB_HOST", "postgres")
    db_port = int(os.environ.get("DB_PORT", 5432))
    db_name = os.environ.get("DB_NAME", "mydatabase")
    db_user = os.environ.get("DB_USER", "myuser")
    db_password = os.environ.get("DB_PASSWORD", "mypassword")

    with PostgresConnectorContextManager(
        db_host=db_host,
        db_name=db_name,
        db_user=db_user,
        db_password=db_password,
        db_port=db_port
    ) as db:
        df = db.get_data_sql("SELECT * FROM facilities LIMIT 5;")
        assert not df.empty, "No data returned from facilities table"