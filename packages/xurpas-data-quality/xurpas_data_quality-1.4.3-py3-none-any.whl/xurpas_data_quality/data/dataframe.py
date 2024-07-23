import os
import warnings

import pandas as pd
from pyspark.sql.functions import to_timestamp

def load_csv(file_path, **kwargs):
    return pd.read_csv(file_path)

def load_excel(file_path, **kwargs):
    return pd.read_excel(file_path, **kwargs)

def load_parquet(file_path, **kwargs):
    return pd.read_parquet(file_path, **kwargs)

def load_orc(file_path, **kwargs):
    return pd.read_orc(file_path, **kwargs)

def validate_dataframe(df: pd.DataFrame) -> bool:
    """
    Checks if dataframe is empty.

    Args
        df: dataframe to validate

    Returns
        A boolean. False if the dataframe is empty, True if otherwise
    """
    if df.empty:
        warnings.warn("DataFrame is empty! Generating Empty Report")
        return False
    else:
        return True

def load_dataframe(file_path: str) -> pd.DataFrame:
    load_methods = {
    '.csv': load_csv,
    '.xlsx': load_excel,
    '.parquet': load_parquet,
    '.orc': load_orc
    }
    # Get the file extension
    _, file_extension = os.path.splitext(file_path)
    
    # Get the loading method from the dictionary
    load_method = load_methods.get(file_extension)
    
    # If the loading method exists, call it, else raise an error
    if load_method:
        return load_method(file_path)
    else:
        raise ValueError(f'Unsupported file format: {file_extension}')

def convert_to_pandas(spark_df):
    """
    Converts to pandas dataframe the spark_df
    """
    try:
        df = spark_df.toPandas()

        return df

    except pd.errors.OutOfBoundsDatetime as e:
        print(f"ERROR: {e}")
        for column, dtype in spark_df.dtypes:
            if dtype =='timestamp':
                spark_df = spark_df.withColumn(column, to_timestamp(spark_df[column], 'yyyy-MM-dd HH:mm:ss'))
        
        df = spark_df.toPandas()

        return df

    
