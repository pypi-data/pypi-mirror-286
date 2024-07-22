from assertpy import assert_that

from tests.global_test_data import df_global

from data_quality_kit.validate_nulls import check_nulls

def test_nulls_present():
    assert_that(check_nulls(df_global, 'column2')).is_true()

def test_no_nulls():
    assert_that(check_nulls(df_global, 'column1')).is_false()
    assert_that(check_nulls(df_global, 'column3')).is_false()

def test_invalid_column_type():
    error_msg = 'Error: Field name must be a string.'
    assert_that(check_nulls).raises(TypeError).when_called_with(
        df_global, 123
    ).is_equal_to(error_msg)

def test_invalid_column_name():
    error_msg = 'Error: Field "nonexistent" not in DataFrame.'
    assert_that(check_nulls).raises(ValueError).when_called_with(
        df_global, "nonexistent"
    ).is_equal_to(error_msg)
    