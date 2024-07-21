"""
various df functions to create scores of df data
"""
import numpy as np
import pandas as pd
from typing import Union


def df_to_cross_sectional_score(df: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
    """
    compute cross sectional score
    """
    if isinstance(df, pd.Series):
        score = (df - np.nanmean(df)) / np.nanstd(df)
    else:
        score = (df - np.nanmean(df, axis=1, keepdims=True)) / np.nanstd(df, axis=1, keepdims=True)
    return score


def df_to_max_score(df: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
    """
    normalized rows by cross-sectional max: max element = 1.0
    """
    if isinstance(df, pd.Series):
        score = df.divide(np.nanmax(df, axis=0))
    else:
        score = df.divide(np.nanmax(df, axis=1, keepdims=True))
    return score
