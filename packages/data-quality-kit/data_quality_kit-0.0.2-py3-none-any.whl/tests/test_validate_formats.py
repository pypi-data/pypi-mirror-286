from assertpy import assert_that

from tests.global_test_data import df_global

from data_quality_kit.validate_formats import check_type_format

def test_correct_type():
    assert_that(check_type_format(df_global, 'column1', int)).is_true()
    assert_that(check_type_format(df_global, 'column3', str)).is_true()

def test_incorrect_type():
    assert_that(check_type_format(df_global, 'column3', int)).is_false()
    assert_that(check_type_format(df_global, 'column2', str)).is_false()

def test_nonexistent_column():
    error_msg = 'Column "nonexistent" not in DataFrame.'
    assert_that(check_type_format).raises(ValueError).when_called_with(
        df_global, "nonexistent", int
    ).is_equal_to(error_msg)