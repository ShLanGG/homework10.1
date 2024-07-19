from time import time
import sys
from functools import wraps


def log(filename=None):
    log_file = filename if filename else sys.stdout

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                start_time = time()
                result = func(*args, **kwargs)
                end_time = time()

                if isinstance(log_file, str):
                    with open(log_file, 'a') as f:
                        f.write(f"{func.__name__} ok\n"
                                f"Time for work: {end_time - start_time}\n")
                else:
                    print(f"{func.__name__} ok\n"
                          f"Time for work: {end_time - start_time}\n",
                          file=log_file)

                return result

            except Exception as e:
                error_type = type(e).__name__
                inputs = (args, kwargs)
                if isinstance(log_file, str):
                    with open(log_file, 'a') as f:
                        f.write(f"{func.__name__} error: {error_type}. Inputs: {inputs}\n")
                else:
                    print(f"{func.__name__} error: {error_type}. Inputs: {inputs}", file=log_file)

                raise

        return wrapper

    return decorator
