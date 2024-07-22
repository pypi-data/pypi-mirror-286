import pandas as pd
from pandas import DataFrame


def df_is_empty(df: DataFrame) -> bool:
    """
    Check if a DataFrame is empty.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to check for emptiness.

    Returns
    -------
    bool
        True if the DataFrame is empty, False otherwise.
    """
    return df.empty
