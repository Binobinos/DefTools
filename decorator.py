import datetime
from typing import Iterable, TypeVar

_T = TypeVar('_T')  # Объявляем типовую переменную

def logger(default: any):
    def timer(func):

        def wrapper(*args, **kwargs):
            start = datetime.datetime.now()
            error = None
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                result = default
                error = e
            print(f"[{start}] - [{datetime.datetime.now() - start}]  {func.__name__}(args={args}, kwargs={kwargs}) "
                  f"-> {result} - \033[5;31mErrors: {str(error).title()}\033[0m")

        return wrapper

    return timer


def cache(time: str):
    cashe = {}

    def timer(func):

        def wrapper(*args, **kwargs):
            if func in cashe:
                if {"args": args, "kwargs": kwargs} in cashe[func]:
                    print(f"Сохраняем {func.__name__} c {cashe[func]["args"]}")
                    cashe[func]["args"] = [{"args": args, "kwargs": kwargs}]
                    cashe[func]["args"].append(func(*args, **kwargs))
                else:
                    print("Кешируем")
            else:
                print("Сохраняем")
                cashe[func] = {}
                cashe[func][{"args": args, "kwargs": kwargs}] = func(*args, **kwargs)
            print(cashe)
            return cashe[func]["args"][1]

        return wrapper

    return timer


@cache("30 min")
def sums(a, b):
    return a + b


def xenumerate(iterable: Iterable[_T],
               *,
               start: int | float = 0,
               step: int | float = 1,
               reverse: bool = False):
    """
    Улучшенная версия enumerate
    :param iterable: Итерируемый обьект
    :param start: Старт
    :param step: Шаг
    :param reverse: Развернутый список
    :return: Генератор
    """
    iterable, num = iterable if not reverse else iterable[::-1], start
    for item in iterable:
        yield num, item
        num += step


def xrange(*params):
    """

    :param end:
    :param start:
    :param step:
    :return:
    """
    len_param = len(params)
    if len_param == 1:
        start, end, step, rounds = 1, params[0], 1, 0
    elif len_param == 2:
        start, end, step, rounds = params[0], params[1], 1, 0
    elif len_param == 3:
        start, end, step, rounds = params[0], params[1], params[2], len(str(params[2] % 1)[2:])
    else:
        if not len_param:
            raise TypeError(f"TypeError: range expected at least 1 argument, got 0")
        else:
            raise TypeError(f"range expected at most 3 arguments, got {len(params)}")
    num = start
    if step > 0:
        while num <= end:
            yield round(num, rounds)
            num += step
    elif step < 0:
        while num >= end:
            yield round(num, rounds)
            num += step
    else:
        raise ValueError("xrange() arg 3 must not be zero")


# пример с xenumerate

list_nums = [1, 2, 3, 4, 5]
for i in xenumerate(list_nums, start=1.5, step=0.1, reverse=True):
    print(i)

# пример с xrange
for i in xrange(23, 7, 0):
    print(i)
