import functools
import logging
from datetime import datetime
from typing import Optional, Callable, Any
import pandas as pd

logger = logging.getLogger(__name__)


def log(filename: str = "") -> any:
    """Decorator create log about function operation."""

    def my_decorator(func: any):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if filename:
                    with open(filename, "w") as file:
                        file.write(f"{func.__name__} ok")
                else:
                    print(f"{func.__name__} ok")
                return result
            except Exception as e:
                if filename:
                    with open(filename, "w") as file:
                        file.write(f"{func.__name__} error: {e.__class__.__name__}. Inputs: {args}, {kwargs}")
                else:
                    print(f"{func.__name__} error: {e.__class__.__name__}. Inputs: {args}, {kwargs}")

        return wrapper

    return my_decorator


def report_to_file(filename: Optional[str] = None) -> Callable:
    """Декоратор для сохранения результата отчёта в CSV (или JSON)."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            if filename:
                fname = filename
            else:
                fname = f"{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            try:
                if isinstance(result, pd.DataFrame):
                    result.to_csv(fname, index=False)
                elif isinstance(result, dict):
                    import json
                    with open(fname, 'w', encoding='utf-8') as f:
                        json.dump(result, f, ensure_ascii=False, default=str)
                else:
                    with open(fname, 'w', encoding='utf-8') as f:
                        f.write(str(result))
                logger.info(f"Отчёт сохранён в {fname}")
            except Exception as e:
                logger.error(f"Ошибка сохранения отчёта: {e}")
            return result
        return wrapper
    return decorator
