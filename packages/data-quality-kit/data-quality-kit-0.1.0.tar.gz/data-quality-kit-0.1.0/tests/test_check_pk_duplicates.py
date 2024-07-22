from assertpy import assert_that

from tests.global_test_data import df_global

from data_quality_kit.check_pk_duplicates import check_no_duplicates

def test_no_duplicates():
    assert_that(check_no_duplicates(df_global, 'unique_ids')).is_false()

def test_duplicates():
    assert_that(check_no_duplicates(df_global, 'duplicated_ids')).is_true()

def test_invalid_column_name():
    error_msg = 'Column "nonexistent" not in DataFrame.'
    assert_that(check_no_duplicates).raises(ValueError).when_called_with(
        df_global, "nonexistent"
    ).is_equal_to(error_msg)
