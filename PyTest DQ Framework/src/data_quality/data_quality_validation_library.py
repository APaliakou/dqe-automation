import pandas as pd

class DataQualityLibrary:

    @staticmethod
    def check_duplicates(df, column_names=None):
        if column_names:
            duplicates = df.duplicated(subset=column_names)
        else:
            duplicates = df.duplicated()
        assert not duplicates.any(), f"Found duplicates in columns {column_names if column_names else 'all columns'}"

    @staticmethod
    def check_count(df1, df2):
        assert len(df1) == len(df2), f"Row count mismatch: {len(df1)} (source) vs {len(df2)} (target)"

    @staticmethod
    def check_data_full_data_set(df1, df2):
        missing = pd.concat([df1, df2, df2]).drop_duplicates(keep=False)
        assert missing.empty, f"Missing rows in target data: {missing}"

    @staticmethod
    def check_dataset_is_not_empty(df):
        assert not df.empty, "Dataset is empty"

    @staticmethod
    def check_not_null_values(df, column_names=None):
        columns = column_names if column_names else df.columns
        for col in columns:
            assert df[col].notnull().all(), f"Null values found in column: {col}"