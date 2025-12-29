import pandas as pd
import os

class ParquetReader:
    def process(self, path, include_subfolders=True):
        dfs = []
        if include_subfolders:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.parquet'):
                        print(f"Reading file: {os.path.join(root, file)}")  # <-- subfolders
                        dfs.append(pd.read_parquet(os.path.join(root, file)))
        else:
            for file in os.listdir(path):
                if file.endswith('.parquet'):
                    print(f"Reading file: {os.path.join(path, file)}")  # <-- no subfolders
                    dfs.append(pd.read_parquet(os.path.join(path, file)))
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        else:
            return pd.DataFrame()