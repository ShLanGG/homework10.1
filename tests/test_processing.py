import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize('state', [
    'EXECUTED',
    'CANCELED',
    'EXECUTED',
    'CANCELED'
])
def test_filter_by_state(list_for_processing, state):
    assert filter_by_state(list_for_processing, state)


def test_filter_without_state(list_for_processing_without_state):
    assert filter_by_state(list_for_processing_without_state) == []


def test_sort_by_date(list_for_processing):
    assert sort_by_date(list_for_processing)


def test_sort_by_same_date():
    assert sort_by_date([{'id': 594226727, 'state': '', 'date': '2019-07-03T18:35:29.512364'},
                         {'id': 41428829, 'state': '', 'date': '2019-07-03T18:35:29.512364'},
                         {'id': 939719570, 'state': '', 'date': '2018-06-30T02:08:58.425572'},
                         {'id': 615064591, 'state': '', 'date': '2018-10-14T08:21:33.419441'}])


def test_sort_by_date_errors(list_for_sort_by_date_with_errors):
    with pytest.raises(ValueError) as exc_info:
        sort_by_date(list_for_sort_by_date_with_errors)

    assert str(exc_info.value) == 'Есть неккоректная дата(-ы)'
