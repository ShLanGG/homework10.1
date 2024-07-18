import pytest

from src.widget import get_data, mask_account_card


@pytest.mark.parametrize('user_information, expected_result', [
    ('Maestro 1596 8378 6870 5199', 'Maestro 1596 83** **** 5199'),
    ('Счет 64686473678894779589', 'Счет **9589'),
    ('MasterCard 7158300734726758', 'MasterCard 7158 30** **** 6758'),
    ('Счет 35383033474447895560', 'Счет **5560'),
    ('Visa Classic 6831 9824 7673 7658', 'Visa Classic 6831 98** **** 7658'),
    ('Visa Classic 1234123412341234', 'Visa Classic 1234 12** **** 1234')
])
def test_mask_account_card(user_information, expected_result):
    assert mask_account_card(user_information) == expected_result


@pytest.mark.parametrize('faults', [
    '',
    'Счет',
    '12341234123412341234',
    '1',
    '1234 1234 1234 1234',
    'Maestro **12351',
])
def test_mask_account_faults(faults):
    with pytest.raises(ValueError) as exc_info:
        mask_account_card(faults)

    assert str(exc_info.value) == "Введены некорректные данные!"


def test_get_data():
    assert get_data('2023-11-14T02:26:18.671407') == '14.11.2023'
    assert get_data('2024-07-17iruaghpairueghiuh') == '17.07.2024'
    assert get_data('2024-07-17i') == '17.07.2024'


def test_get_data_errors():
    with pytest.raises(ValueError) as exc_info:
        get_data('')

    assert str(exc_info.value) == 'Введён неправильный формат даты'

    with pytest.raises(ValueError) as exc_info:
        get_data('2024-')

    assert str(exc_info.value) == 'Введён неправильный формат даты'

    with pytest.raises(ValueError) as exc_info:
        get_data('20ii-123-1234eiirhuf')

    assert str(exc_info.value) == 'Введён неправильный формат даты'