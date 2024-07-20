import pytest
from time import sleep
from src.decorators import log


# Тестовая функция для успешного выполнения
@log()
def test_function_success(x, y):
    sleep(0.1)  # для проверки времени выполнения
    return x + y


# Тестовая функция для генерации исключения
@log()
def test_function_error(x, y):
    raise ValueError("Test error")


def test_log_success(capsys):
    result = test_function_success(1, 2)
    captured = capsys.readouterr()

    assert result == 3
    assert captured.out == "test_function_success ok\nTime for work: 0.1\n"


def test_log_error(capsys):
    with pytest.raises(ValueError, match="Test error"):
        test_function_error(1, 2)

    captured = capsys.readouterr()
    assert "test_function_error error: ValueError. Inputs: ((1, 2), {})" in captured.out


def test_log_to_file(tmpdir):
    log_file = tmpdir.join("test_log.txt")

    # Тестовая функция для успешного выполнения с логированием в файл
    @log(filename=str(log_file))
    def test_function_file_success(x, y):
        sleep(0.1)  # для проверки времени выполнения
        return x + y

    # Тестовая функция для генерации исключения с логированием в файл
    @log(filename=str(log_file))
    def test_function_file_error(x, y):
        raise ValueError("Test error")

    test_function_file_success(1, 2)
    with pytest.raises(ValueError, match="Test error"):
        test_function_file_error(1, 2)

    with open(str(log_file), 'r') as f:
        log_content = f.read()
    assert "test_function_file_success ok" in log_content
    assert "Time for work" in log_content
    assert "test_function_file_error error: ValueError. Inputs: ((1, 2), {})" in log_content
