import pytest
from src.connectors.postgres.postgres_connector import PostgresConnectorContextManager
from src.connectors.file_system.parquet_reader import ParquetReader

def pytest_addoption(parser):
    parser.addoption("--db_host", action="store", default="localhost", help="Database host")
    parser.addoption("--db_name", action="store", default="mydatabase", help="Database name")
    parser.addoption("--db_port", action="store", default="5432", help="Database port")
    parser.addoption("--db_user", action="store", default="myuser", help="Database user")
    parser.addoption("--db_password", action="store", default="mypassword", help="Database password")

def pytest_configure(config):
    required_options = ["db_user", "db_password"]
    for option in required_options:
        if not config.getoption(option):
            pytest.fail(f"Missing required option: {option}")

@pytest.fixture(scope='session')
def db_connection(request):
    db_host = request.config.getoption("db_host")
    db_name = request.config.getoption("db_name")
    db_port = request.config.getoption("db_port")
    db_user = request.config.getoption("db_user")
    db_password = request.config.getoption("db_password")
    try:
        with PostgresConnectorContextManager(
            db_host=db_host,
            db_name=db_name,
            db_user=db_user,
            db_password=db_password,
            db_port=db_port
        ) as db_connector:
            yield db_connector
    except Exception as e:
        pytest.fail(f"Failed to initialize PostgresConnectorContextManager: {e}")

@pytest.fixture(scope='session')
def parquet_reader():
    return ParquetReader()

@pytest.fixture(scope='module')
def source_facility_name_min_time_spent_per_visit_date(db_connection):
    sql = """
        SELECT
            f.facility_name,
            TO_CHAR(DATE(v.visit_timestamp), 'YYYY-MM') AS visit_date,
            MIN(v.duration_minutes) AS avg_time_spent
        FROM visits v
        JOIN facilities f ON v.facility_id = f.id
        GROUP BY f.facility_name, TO_CHAR(DATE(v.visit_timestamp), 'YYYY-MM')
    """
    return db_connection.get_data_sql(sql)

@pytest.fixture(scope='module')
def target_facility_name_min_time_spent_per_visit_date(parquet_reader):
    path = '/parquet_data/facility_name_min_time_spent_per_visit_date'
    return parquet_reader.process(path, include_subfolders=True)

@pytest.fixture(scope='module')
def source_patient_sum_treatment_cost_per_facility_type(db_connection):
    sql = """
        SELECT
            f.facility_type,
            p.first_name || ' ' || p.last_name AS full_name,
            SUM(v.treatment_cost) AS sum_treatment_cost
        FROM visits v
        JOIN facilities f ON v.facility_id = f.id
        JOIN patients p ON v.patient_id = p.id
        GROUP BY f.facility_type, p.first_name, p.last_name
    """
    return db_connection.get_data_sql(sql)

@pytest.fixture(scope='module')
def target_patient_sum_treatment_cost_per_facility_type(parquet_reader):
    path = '/parquet_data/patient_sum_treatment_cost_per_facility_type'
    return parquet_reader.process(path, include_subfolders=True)