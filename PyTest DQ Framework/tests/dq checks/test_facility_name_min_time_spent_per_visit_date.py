import pytest
import pandas as pd

@pytest.mark.parquet_data
@pytest.mark.smoke
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_dataset_is_not_empty(target_facility_name_min_time_spent_per_visit_date):
    assert not target_facility_name_min_time_spent_per_visit_date.empty

@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_row_count(source_facility_name_min_time_spent_per_visit_date, target_facility_name_min_time_spent_per_visit_date):
    assert len(source_facility_name_min_time_spent_per_visit_date) == len(target_facility_name_min_time_spent_per_visit_date)

@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_schema(source_facility_name_min_time_spent_per_visit_date, target_facility_name_min_time_spent_per_visit_date):
    assert list(source_facility_name_min_time_spent_per_visit_date.columns) == list(target_facility_name_min_time_spent_per_visit_date.columns)

@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_not_null(target_facility_name_min_time_spent_per_visit_date):
    for col in ['facility_name', 'visit_date', 'avg_time_spent']:
        assert target_facility_name_min_time_spent_per_visit_date[col].notnull().all()

@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_uniqueness(target_facility_name_min_time_spent_per_visit_date):
    assert not target_facility_name_min_time_spent_per_visit_date.duplicated(['facility_name', 'visit_date']).any()

@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_avg_time_spent_positive(target_facility_name_min_time_spent_per_visit_date):
    assert (target_facility_name_min_time_spent_per_visit_date['avg_time_spent'] > 0).all()

@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_visit_date_format(target_facility_name_min_time_spent_per_visit_date):
    assert target_facility_name_min_time_spent_per_visit_date['visit_date'].apply(lambda x: pd.to_datetime(x, format='%Y-%m', errors='coerce')).notnull().all()

@pytest.mark.parquet_data
@pytest.mark.facility_name_min_time_spent_per_visit_date
def test_data_equality(source_facility_name_min_time_spent_per_visit_date, target_facility_name_min_time_spent_per_visit_date):
    merged = pd.merge(
        source_facility_name_min_time_spent_per_visit_date,
        target_facility_name_min_time_spent_per_visit_date,
        on=['facility_name', 'visit_date'],
        how='outer',
        suffixes=('_src', '_tgt'),
        indicator=True
    )
    assert (merged['_merge'] == 'both').all()
    assert (merged['avg_time_spent_src'] == merged['avg_time_spent_tgt']).all()