import pandas as pd

def check_no_duplicates(df: pd.DataFrame, pk_column: str) -> bool:
    """
    Checks for duplicate values in the specified primary key column of a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to check.
    pk_column (str): The name of the primary key column to check for duplicates.

    Returns:
    bool: True if there are duplicate values in the primary key column, False if there are no duplicates.

    Raises:
    ValueError: If the pk_column is not a column in the DataFrame.
    """
    if pk_column not in df.columns:
        raise ValueError(f'Column "{pk_column}" not in DataFrame.')
    
    return df[pk_column].duplicated().any()

