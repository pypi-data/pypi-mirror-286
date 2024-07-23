import pandas as pd
import numpy as np


def drop_columns_based_on_mean(dataframe: pd.DataFrame):
    # Compute the mean of each column
    column_means = dataframe.mean()

    # Identify columns where the mean is 0
    columns_to_drop = column_means[column_means == 0].index

    # Drop these columns from the DataFrame
    dataframe = dataframe.drop(columns=columns_to_drop)

    return dataframe.columns


def drop_infinity_columns(dataframe: pd.DataFrame):
    dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)

    dataframe.dropna(inplace=True)

    return dataframe


def write_column_datatypes_to_txt(dataframe: pd.DataFrame, fileLoc: str):
    """Writes the datatype of each column in a DataFrame to a text file.

    Args:
      df: The pandas DataFrame.
      "fileLoc": The name of the output text file.
    """

    with open(fileLoc, "w") as f:
        for col, dtype in dataframe.dtypes.items():
            f.write(f"{col}: {dtype}\n")


def dataframe_check(dataframe:pd.DataFrame): 
    rows_with_nan = dataframe[dataframe.isnull().any(axis=1)]

    nan_counts = dataframe.isnull().sum()

    has_nan = dataframe.isnull().values.any()

    has_inf = dataframe.isin([np.inf, -np.inf]).any().any()
    rows_with_inf = dataframe[dataframe.isin([np.inf, -np.inf]).any(axis=1)]
    
    duplicated_rows = dataframe[dataframe.duplicated()]
    has_duplicates = duplicated_rows.shape[0] > 0
    
    data_types = dataframe.dtypes
    
    zero_counts = (dataframe == 0).sum()
    has_zero = (dataframe == 0).values.any()
    
    
    return {
        'rows_with_nan': rows_with_nan,
        'nan_counts': nan_counts,
        'has_nan': has_nan,
        'has_inf': has_inf,
        'rows_with_inf': rows_with_inf,
        'duplicated_rows': duplicated_rows,
        'has_duplicates': has_duplicates,
        'data_types': data_types,
        'zero_counts': zero_counts,
        'has_zero': has_zero,
    }