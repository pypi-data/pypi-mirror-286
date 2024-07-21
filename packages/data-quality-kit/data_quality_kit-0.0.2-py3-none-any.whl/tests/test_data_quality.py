from assertpy import assert_that 

from tests.global_test_data import df_global  

from data_quality_kit.data_quality import df_is_empty  

def test_df_is_empty():
    df_empty = df_global.iloc[0:0]
    assert_that(df_is_empty(df_empty)).is_true()

def test_df_is_not_empty():
    assert_that(df_is_empty(df_global)).is_false()
