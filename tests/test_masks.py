import pytest

from src.masks import get_mask_account, get_mask_card_number

def test_get_mask_card_number():
    assert get_mask_card_number('1234123412341234') == '1234 12** **** 1234'
    assert get_mask_card_number('1596 8378 6870 5199') == '1596 83** **** 5199'

def test_get_mask_card_number_letter():
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number('abcdabcdabcdabcd')

    assert str(exc_info.value) == "Длина номера карты только 16 ЦИФР"


def test_get_mask_card_number_length():
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number('12341234123412341234')

    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number('1234 1234 1234 1234 1234')

    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number('1234 1234 1234 ')

    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number('')

    assert str(exc_info.value) == "Длина номера карты только 16 ЦИФР"


def test_get_mask_account():
    assert get_mask_account('12341234123412341234') == '**1234'
    assert get_mask_account('8617234528346758237465283476') == '**3476'


def test_get_mask_account_short_length():
    with pytest.raises(ValueError) as exc_info:
        get_mask_account('1234123412341234')

    assert str(exc_info.value) == "Длина счета минимум 20 ЦИФР"


def test_get_mask_account_letters():
    with pytest.raises(ValueError) as exc_info:
        get_mask_account('abcdabcdabcdabcdabcd')

    assert str(exc_info.value) == "Длина счета минимум 20 ЦИФР"