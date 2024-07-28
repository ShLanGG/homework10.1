import pytest

from src.decorators import log


# Тестовая функция для успешного выполнения
@log()
def test_function_success(x, y):
    return x + y


# Тестовая функция для генерации исключения
@log()
def test_function_error(x, y):
    raise ValueError("Test error")


def test_log_success(capsys):
    test_function_success(1, 2)

    captured = capsys.readouterr()
    assert captured.out == "test_function_success ok\n"


def test_log_error(capsys):
    test_function_error(1, 2)

    captured = capsys.readouterr()
    assert "test_function_error error: ValueError. Inputs: (1, 2), {}\n" in captured.out


def test_log_to_file(tmpdir):
    log_file = tmpdir.join("test_log.txt")

    # Тестовая функция для успешного выполнения с логированием в файл
    @log(filename=str(log_file))
    def test_function_file_success(x, y):
        return x + y

    # Тестовая функция для генерации исключения с логированием в файл
    @log(filename=str(log_file))
    def test_function_file_error(x, y):
        raise ValueError("Test error")

    #Проверка вывода в файл правильную работу функции
    test_function_file_success(1, 2)

    with open(str(log_file), 'r') as f:
        log_content = f.read()

    assert "test_function_file_success ok" in log_content

    # Проверка вывода в файл ошибочную работу функции
    test_function_file_error(1, 2)

    with open(str(log_file), 'r') as f:
        log_content = f.read()

    assert "test_function_file_error error: ValueError. Inputs: (1, 2), {}" in log_content
