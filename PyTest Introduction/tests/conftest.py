import pytest
import pandas as pd

def pytest_collection_modifyitems(session, config, items):
    for item in items:
        if not item.own_markers:
            item.add_marker(pytest.mark.unmarked)

@pytest.fixture(scope="session")
def csv_data(request):
    path = getattr(request, 'param', "PyTest Introduction/src/data/data.csv")
    return pd.read_csv(path)

@pytest.fixture(scope="session")
def expected_schema():
    return ["id", "name", "age", "email", "is_active"]

@pytest.fixture(scope="session")
def validate_schema():
    def _validate(actual_schema, expected_schema):
        return set(actual_schema) == set(expected_schema)
    return _validate