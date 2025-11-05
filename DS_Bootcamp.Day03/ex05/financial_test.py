from financial import get_info
import pytest

def test_ticker_correct():
    res = get_info('MSFT', 'Total Revenue')
    assert res[0] == 'Total Revenue'
    assert res[1] is not None

def test_type_correct():
    res = get_info('MSFT', 'Total Revenue')
    assert type(res) == tuple

def test_ticker_incorrect():
    with pytest.raises(ValueError):
        get_info('Error', 'Total Revenue')

def test_field_incorrect():
    with pytest.raises(AttributeError):
        get_info('MSFT', 'Error')

if __name__ == '__main__':
    test_ticker_correct()
    test_type_correct()
    test_ticker_incorrect()
    test_field_incorrect()