"""
Лабораторная работа № 1. Вариант 0.
Итерационные методы вычисления √a, ∛b, ln c.
"""
import math

EPS = 1e-6
N_MAX = 100


def sqrt_newton(a, eps=EPS, n_max=N_MAX):
    """Квадратный корень методом Ньютона (формула Герона)."""
    if a < 0:
        raise ValueError("Подкоренное выражение должно быть неотрицательным")
    if a == 0:
        return 0.0, 0
    x = a if a >= 1 else 1.0
    for n in range(1, n_max + 1):
        x_new = 0.5 * (x + a / x)
        if abs(x_new - x) < eps:
            return x_new, n
        x = x_new
    raise RuntimeError("Точность не достигнута за N_MAX итераций")


def cbrt_newton(b, eps=EPS, n_max=N_MAX):
    """Кубический корень методом Ньютона (с учётом знака)."""
    if b == 0:
        return 0.0, 0
    sign = -1 if b < 0 else 1
    b = abs(b)
    x = b if b >= 1 else 1.0
    for n in range(1, n_max + 1):
        x_new = (2 * x + b / (x * x)) / 3
        if abs(x_new - x) < eps:
            return sign * x_new, n
        x = x_new
    raise RuntimeError("Точность не достигнута за N_MAX итераций")


def ln_series(c, eps=EPS, n_max=10_000):
    """Натуральный логарифм через ряд ln((1+y)/(1-y)), y=(c-1)/(c+1)."""
    if c <= 0:
        raise ValueError("Аргумент логарифма должен быть положительным")
    y = (c - 1) / (c + 1)
    y2 = y * y
    power = y          # текущая степень y^(2k+1)
    total = 0.0
    for k in range(n_max):
        term = 2 * power / (2 * k + 1)
        if abs(term) < eps:
            return total, k
        total += term
        power *= y2
    raise RuntimeError("Точность не достигнута за n_max итераций")


if __name__ == "__main__":
    a, b, c = 2, 10, 5
    print(f"{'Функция':<10}{'Аргумент':>10}{'Результат':>16}"
          f"{'Эталон':>16}{'Погрешность':>14}{'Итераций':>10}")
    for name, f, arg, ref in [("sqrt", sqrt_newton, a, math.sqrt(a)),
                              ("cbrt", cbrt_newton, b, b ** (1 / 3)),
                              ("ln", ln_series, c, math.log(c))]:
        val, n = f(arg)
        print(f"{name:<10}{arg:>10}{val:>16.10f}{ref:>16.10f}"
              f"{abs(val - ref):>14.2e}{n:>10}")
