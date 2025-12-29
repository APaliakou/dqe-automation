import pytest
import pandas as pd

@pytest.mark.parquet_data
@pytest.mark.smoke
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_dataset_is_not_empty(target_patient_sum_treatment_cost_per_facility_type):
    assert not target_patient_sum_treatment_cost_per_facility_type.empty

@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_row_count(source_patient_sum_treatment_cost_per_facility_type, target_patient_sum_treatment_cost_per_facility_type):
    assert len(source_patient_sum_treatment_cost_per_facility_type) == len(target_patient_sum_treatment_cost_per_facility_type)

@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_schema(source_patient_sum_treatment_cost_per_facility_type, target_patient_sum_treatment_cost_per_facility_type):
    assert list(source_patient_sum_treatment_cost_per_facility_type.columns) == list(target_patient_sum_treatment_cost_per_facility_type.columns)

@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_not_null(target_patient_sum_treatment_cost_per_facility_type):
    for col in ['facility_type', 'full_name', 'sum_treatment_cost']:
        assert target_patient_sum_treatment_cost_per_facility_type[col].notnull().all()

@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_uniqueness(target_patient_sum_treatment_cost_per_facility_type):
    assert not target_patient_sum_treatment_cost_per_facility_type.duplicated(['facility_type', 'full_name']).any()

@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_sum_treatment_cost_non_negative(target_patient_sum_treatment_cost_per_facility_type):
    assert (target_patient_sum_treatment_cost_per_facility_type['sum_treatment_cost'] >= 0).all()

@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_full_name_format(target_patient_sum_treatment_cost_per_facility_type):
    assert target_patient_sum_treatment_cost_per_facility_type['full_name'].apply(lambda x: isinstance(x, str) and len(x.split()) == 2).all()

@pytest.mark.parquet_data
@pytest.mark.patient_sum_treatment_cost_per_facility_type
def test_data_equality(source_patient_sum_treatment_cost_per_facility_type, target_patient_sum_treatment_cost_per_facility_type):
    merged = pd.merge(
        source_patient_sum_treatment_cost_per_facility_type,
        target_patient_sum_treatment_cost_per_facility_type,
        on=['facility_type', 'full_name'],
        how='outer',
        suffixes=('_src', '_tgt'),
        indicator=True
    )
    assert (merged['_merge'] == 'both').all()
    assert (merged['sum_treatment_cost_src'] == merged['sum_treatment_cost_tgt']).all()