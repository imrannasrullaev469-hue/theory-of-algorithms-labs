"""
Лабораторная работа № 1. Вариант 16.
Итерационные методы вычисления √a, ∛b, ln c.
Доп. задание Д2: сравнение способов выбора x0 (a, a/2, 1).
"""
import math

EPS = 1e-8
N_MAX = 100

# способы выбора начального приближения (Д2)
X0_RULES = {
    "x0 = a": lambda a: a,
    "x0 = a/2": lambda a: a / 2,
    "x0 = 1": lambda a: 1.0,
}


def sqrt_newton(a, eps=EPS, n_max=N_MAX, x0=1.0):
    """Квадратный корень методом Ньютона (формула Герона)."""
    if a < 0:
        raise ValueError("Подкоренное выражение должно быть неотрицательным")
    if a == 0:
        return 0.0, 0
    x = x0
    for n in range(1, n_max + 1):
        x_new = 0.5 * (x + a / x)
        if abs(x_new - x) < eps:
            return x_new, n
        x = x_new
    raise RuntimeError("Точность не достигнута за N_MAX итераций")


def cbrt_newton(b, eps=EPS, n_max=N_MAX, x0=1.0):
    """Кубический корень методом Ньютона (с учётом знака)."""
    if b == 0:
        return 0.0, 0
    sign = -1 if b < 0 else 1
    b = abs(b)
    x = x0
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


def trace(step, x0, arg, ref, eps=EPS, n_max=N_MAX):
    """Печатает ход итераций метода Ньютона: n, x_n, |x_n − x_(n−1)|, |x_n − x*|."""
    x = x0
    print(f"{'n':>3}{'x_n':>24}{'|x_n - x_(n-1)|':>18}{'|x_n - x*|':>14}")
    print(f"{0:>3}{x:>24.15f}{'':>18}{abs(x - ref):>14.2e}")
    for n in range(1, n_max + 1):
        x_new = step(x, arg)
        print(f"{n:>3}{x_new:>24.15f}{abs(x_new - x):>18.2e}"
              f"{abs(x_new - ref):>14.2e}")
        if abs(x_new - x) < eps:
            return
        x = x_new


if __name__ == "__main__":
    a, b, c = 43, 200, 2.5

    print(f"Вариант 16: a = {a}, b = {b}, c = {c}, eps = {EPS:.0e}, x0 = 1\n")
    print(f"{'Функция':<10}{'Аргумент':>10}{'Результат':>20}"
          f"{'Эталон':>20}{'Погрешность':>14}{'Итераций':>10}")
    for name, f, arg, ref in [("sqrt", sqrt_newton, a, math.sqrt(a)),
                              ("cbrt", cbrt_newton, b, b ** (1 / 3)),
                              ("ln", ln_series, c, math.log(c))]:
        val, n = f(arg)
        print(f"{name:<10}{arg:>10}{val:>20.14f}{ref:>20.14f}"
              f"{abs(val - ref):>14.2e}{n:>10}")

    # Д2: число итераций при разных x0
    print("\nД2. Число итераций при разных начальных приближениях")
    print(f"{'Функция':<10}" + "".join(f"{rule:>12}" for rule in X0_RULES))
    for name, f, arg in [("sqrt", sqrt_newton, a), ("cbrt", cbrt_newton, b)]:
        row = f"{name:<10}"
        for rule in X0_RULES.values():
            row += f"{f(arg, x0=rule(arg))[1]:>12}"
        print(row)

    print("\nПогрешность |x - x*| при разных x0")
    for name, f, arg, ref in [("sqrt", sqrt_newton, a, math.sqrt(a)),
                              ("cbrt", cbrt_newton, b, b ** (1 / 3))]:
        row = f"{name:<10}"
        for rule in X0_RULES.values():
            row += f"{abs(f(arg, x0=rule(arg))[0] - ref):>12.2e}"
        print(row)

    print(f"\nХод итераций для sqrt({a}), x0 = 1")
    trace(lambda x, s: 0.5 * (x + s / x), 1.0, a, math.sqrt(a))
    print(f"\nХод итераций для cbrt({b}), x0 = 1")
    trace(lambda x, s: (2 * x + s / (x * x)) / 3, 1.0, b, b ** (1 / 3))
