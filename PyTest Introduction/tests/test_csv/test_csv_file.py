import pytest
import re

def test_file_not_empty(csv_data):
    assert not csv_data.empty, "Failed: input file is empty"

@pytest.mark.validate_csv
@pytest.mark.xfail(reason="Duplicates in the file")
def test_duplicates(csv_data):
    duplicates = csv_data.duplicated().sum()
    assert duplicates == 0, f"Failed: {duplicates} duplicated rows in the file"

@pytest.mark.validate_csv
def test_validate_schema(csv_data, expected_schema):
    assert set(csv_data.columns) == set(expected_schema), f"Failed: schema mismatch for {csv_data.columns}"

@pytest.mark.validate_csv
@pytest.mark.skip(reason="Age validation disabled")
def test_age_column_valid(csv_data):
    invalid_ages = csv_data[~csv_data["age"].apply(lambda x: str(x).isdigit() and 0 <= int(x) <= 100)]
    assert invalid_ages.empty, f"Failed: invalid age values: {invalid_ages['age'].tolist()}"

@pytest.mark.validate_csv
def test_email_column_valid(csv_data):
    email_regex = r"^[^@]+@[^@]+\.[^@]+$"
    invalid_emails = csv_data[~csv_data["email"].str.match(email_regex)]
    assert invalid_emails.empty, f"Failed: invalid emails found for {invalid_emails['email'].tolist()}"

@pytest.mark.parametrize("id, is_active", [(1, False), (2, True)])
def test_active_players(csv_data, id, is_active):
    row = csv_data[csv_data["id"] == id]
    assert row.iloc[0]["is_active"] == str(is_active), f"Failed: is_active for id={id} should be {is_active}"

def test_active_player(csv_data):
    row = csv_data[csv_data["id"] == 2]
    assert row.iloc[0]["is_active"] == "True", "Failed: is_active for id=2 should be True"