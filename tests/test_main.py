import pytest
from src.main import main, filter_by_status

# Пример данных для проверки вспомогательной функции
sample_transactions = [
    {"state": "EXECUTED", "description": "Покупка"},
    {"state": "CANCELED", "description": "Возврат"},
    {"state": "PENDING", "description": "Ожидание"},
]

def test_filter_by_status_exact():
    filtered = filter_by_status(sample_transactions, "EXECUTED")
    assert len(filtered) == 1
    assert filtered[0]["description"] == "Покупка"

def test_filter_by_status_case_insensitive():
    filtered = filter_by_status(sample_transactions, "pending")
    assert len(filtered) == 1
    assert filtered[0]["description"] == "Ожидание"

def test_filter_nonexistent_status():
    filtered = filter_by_status(sample_transactions, "UNKNOWN")
    assert filtered == []

# Тест main с имитацией ввода
def test_main_flow_json(monkeypatch, capsys):
    # Создадим временный JSON-файл
    import json
    import tempfile
    import os
    
    data = [
        {
            "date": "01.01.2023",
            "state": "EXECUTED",
            "description": "Тестовый перевод",
            "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
            "from": "Счет 123",
            "to": "Счет 456"
        }
    ]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8') as f:
        json.dump(data, f)
        tmp_path = f.name
    
    try:
        inputs = iter([
            '1',                    # выбор JSON
            tmp_path,               # путь
            'executed',             # статус
            'нет',                  # сортировка
            'нет',                  # рублёвые
            'нет'                   # фильтр по слову
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        main()
        captured = capsys.readouterr()
        assert "Всего банковских операций в выборке: 1" in captured.out
        assert "Тестовый перевод" in captured.out
    finally:
        os.unlink(tmp_path)

def test_main_empty_result(monkeypatch, capsys):
    data = []  # пустой файл
    import json, tempfile, os
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8') as f:
        json.dump(data, f)
        tmp_path = f.name
    
    try:
        inputs = iter([
            '1',
            tmp_path,
            'executed',
            'нет',
            'нет',
            'нет'
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        main()
        captured = capsys.readouterr()
        assert "Не найдено ни одной транзакции" in captured.out
    finally:
        os.unlink(tmp_path)