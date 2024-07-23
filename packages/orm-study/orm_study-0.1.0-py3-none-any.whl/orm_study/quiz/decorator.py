import time
from typing import Any, Tuple


class TimeTrace:
    """
    :param func: 파이썬 함수
    :param *args: func 함수의 arguments
    :param **kwargs: func 함수의 keyword arguments
    :return: func의 반환값, func 함수의 실행 시간
    """

    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, *args, **kwargs) -> Tuple[Any, float]:
        start_time = time.time()
        result = self.func(*args, **kwargs)
        end_time = time.time()

        return result, end_time - start_time
