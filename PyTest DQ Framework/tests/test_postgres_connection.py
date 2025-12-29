from src.connectors.postgres.postgres_connector import PostgresConnectorContextManager

def test_postgres_connection():
    db_host = "localhost"
    db_port = 5434
    db_name = "mydatabase"
    db_user = "myuser"
    db_password = "mypassword"

    with PostgresConnectorContextManager(
        db_host=db_host,
        db_name=db_name,
        db_user=db_user,
        db_password=db_password,
        db_port=db_port
    ) as db:
        df = db.get_data_sql("SELECT * FROM facilities LIMIT 5;")
        assert not df.empty, "No data returned from facilities table"