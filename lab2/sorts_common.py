"""Общие функции для генерации данных и замера времени."""
import random
import statistics
import time


def generate_data(n, kind="random", lo=0, hi=100_000, seed=42):
    """Генерирует массив длины n заданного типа."""
    if kind == "duplicates":                 # тип D: много повторов
        lo, hi = 0, 10
    rng = random.Random(seed + n)      # воспроизводимость эксперимента
    data = [rng.randint(lo, hi) for _ in range(n)]
    if kind == "sorted":
        data.sort()
    elif kind == "reversed":
        data.sort(reverse=True)
    elif kind == "nearly_sorted":
        data.sort()
        for _ in range(max(1, n // 20)):          # 5 % случайных перестановок
            i, j = rng.randrange(n), rng.randrange(n)
            data[i], data[j] = data[j], data[i]
    return data


def measure(sort_func, data, repeats=3, reverse=False):
    """Возвращает медианное время работы sort_func на данных data, с.

    При reverse=True функция вызывается как sort_func(data, reverse=True),
    а результат сверяется с sorted(data, reverse=True)."""
    times = []
    expected = sorted(data, reverse=reverse)
    for _ in range(repeats):
        start = time.perf_counter()
        result = sort_func(data, reverse=True) if reverse else sort_func(data)
        times.append(time.perf_counter() - start)
        assert result == expected, f"{sort_func.__name__}: ошибка сортировки"
    return statistics.median(times)
