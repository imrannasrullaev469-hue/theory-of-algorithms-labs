"""
Лабораторная работа № 3. Вариант 16.
Быстрая сортировка (Хоар, опорный — первый элемент) и нисходящая сортировка
слиянием. Сравнение с алгоритмами ЛР № 2 и встроенной sorted().
Доп. задание Г4: максимальная глубина рекурсии на данных R, S, V.
"""
import math
import sys
from pathlib import Path

# модули sorts_common.py и lr2.py лежат в папке ЛР № 2
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lab2"))

from sorts_common import generate_data, measure  # noqa: E402
from lr2 import bubble_sort, insertion_sort      # noqa: E402

LO, HI = 0, 1_000_000             # диапазон значений (как в ЛР № 2)
REPEATS = 5                       # медиана из 5 замеров


# ---------- Быстрая сортировка ----------
def quick_sort(arr):
    a = arr.copy()
    _quick_sort(a, 0, len(a) - 1)
    return a


def _quick_sort(a, lo, hi):
    while lo < hi:
        p = _partition(a, lo, hi)
        # рекурсия в меньшую часть — глубина стека O(log n)
        if p - lo < hi - p:
            _quick_sort(a, lo, p)
            lo = p + 1
        else:
            _quick_sort(a, p + 1, hi)
            hi = p


def _partition(a, lo, hi):
    """Разбиение Хоара, опорный элемент — первый."""
    pivot = a[lo]
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < pivot:
            i += 1
        j -= 1
        while a[j] > pivot:
            j -= 1
        if i >= j:
            return j
        a[i], a[j] = a[j], a[i]


# ---------- Сортировка слиянием ----------
def merge_sort(arr):
    if len(arr) <= 1:
        return arr.copy()
    mid = len(arr) // 2
    return _merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))


def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:          # «<=» обеспечивает устойчивость
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------- Г4: глубина рекурсии ----------
def quick_depth(arr):
    """Максимальная глубина рекурсии quick_sort (рекурсия в меньшую часть)."""
    a = arr.copy()
    max_depth = 0

    def rec(lo, hi, depth):
        nonlocal max_depth
        max_depth = max(max_depth, depth)
        while lo < hi:
            p = _partition(a, lo, hi)
            if p - lo < hi - p:
                rec(lo, p, depth + 1)
                lo = p + 1
            else:
                rec(p + 1, hi, depth + 1)
                hi = p

    rec(0, len(a) - 1, 1)
    return max_depth


def quick_naive_depth(arr):
    """Глубина рекурсии «наивной» быстрой сортировки (два рекурсивных вызова)."""
    a = arr.copy()
    max_depth = 0

    def rec(lo, hi, depth):
        nonlocal max_depth
        max_depth = max(max_depth, depth)
        if lo < hi:
            p = _partition(a, lo, hi)
            rec(lo, p, depth + 1)
            rec(p + 1, hi, depth + 1)

    rec(0, len(a) - 1, 1)
    return max_depth


def merge_depth(arr, depth=1):
    """Максимальная глубина рекурсии merge_sort."""
    if len(arr) <= 1:
        return depth
    mid = len(arr) // 2
    return max(merge_depth(arr[:mid], depth + 1),
               merge_depth(arr[mid:], depth + 1))


# ---------- Эксперименты ----------
def run_experiment(algorithms, sizes, kind="random", repeats=REPEATS):
    results = {name: [] for name in algorithms}
    print(f"{'n':>8}" + "".join(f"{name:>12}" for name in algorithms))
    for n in sizes:
        data = generate_data(n, kind=kind, lo=LO, hi=HI)
        row = f"{n:>8}"
        for name, func in algorithms.items():
            t = measure(func, data, repeats)
            results[name].append(t)
            row += f"{t:>12.5f}"
        print(row)
    return results


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # один цвет на алгоритм во всех графиках
    COLORS = {"Пузырьком": "#2a78d6", "Вставками": "#eb6834",
              "Быстрая": "#1baf7a", "Слиянием": "#eda100",
              "sorted()": "#e87ba4"}
    KINDS = {"random": "R", "sorted": "S", "reversed": "V",
             "nearly_sorted": "N", "duplicates": "D"}

    # Эксперимент 1: четыре алгоритма на размерах из ЛР № 2
    print("Эксперимент 1: четыре алгоритма, случайные данные")
    small = [500, 1500, 2500, 3500, 4500]
    res1 = run_experiment({"Пузырьком": bubble_sort,
                           "Вставками": insertion_sort,
                           "Быстрая": quick_sort,
                           "Слиянием": merge_sort}, small)

    # Эксперимент 2: O(n log n) на больших размерах
    print("\nЭксперимент 2: алгоритмы O(n log n) на больших массивах")
    large = [20_000, 30_000, 40_000, 50_000]
    res2 = run_experiment({"Быстрая": quick_sort,
                           "Слиянием": merge_sort,
                           "sorted()": sorted}, large)
    print(f"\n{'n':>8}{'Слиянием / Быстрая':>22}{'Быстрая / sorted()':>22}")
    for k, n in enumerate(large):
        print(f"{n:>8}{res2['Слиянием'][k] / res2['Быстрая'][k]:>22.2f}"
              f"{res2['Быстрая'][k] / res2['sorted()'][k]:>22.2f}")

    # Проверка роста T(n2)/T(n1)
    print("\nОтношение T(n2)/T(n1)")
    print(f"{'Переход':>18}{'Быстрая':>10}{'Слиянием':>10}"
          f"{'n log n':>10}{'n²':>8}")
    pairs = list(zip(large, large[1:])) + [(large[0], 2 * large[0])]
    for n1, n2 in pairs:
        i, j = large.index(n1), large.index(n2)
        theory = n2 * math.log(n2) / (n1 * math.log(n1))
        print(f"{n1:>8} -> {n2:<7}"
              f"{res2['Быстрая'][j] / res2['Быстрая'][i]:>10.2f}"
              f"{res2['Слиянием'][j] / res2['Слиянием'][i]:>10.2f}"
              f"{theory:>10.2f}{(n2 / n1) ** 2:>8.2f}")

    # Эксперимент 3: влияние структуры данных.
    # Опорный «первый» на S и V даёт Θ(n²), поэтому для всех типов
    # берём n = 3000, а n = 50 000 — только для R, N, D.
    res3 = {}
    for n, kinds in ((3000, KINDS), (50_000, ("random", "nearly_sorted",
                                               "duplicates"))):
        print(f"\nЭксперимент 3, n = {n}")
        for kind in kinds:
            data = generate_data(n, kind=kind, lo=LO, hi=HI)
            tq = measure(quick_sort, data, REPEATS)
            tm = measure(merge_sort, data, REPEATS)
            res3[n, kind] = (tq, tm)
            print(f"{kind:>15} ({KINDS[kind]}): быстрая {tq:.5f} с, "
                  f"слиянием {tm:.5f} с, быстрая / слиянием {tq / tm:.2f}")

    print("\nКвадратичный рост быстрой сортировки на упорядоченных данных (S)")
    deg_sizes = [1000, 2000, 3000, 4000]
    deg = []
    for n in deg_sizes:
        t = measure(quick_sort, generate_data(n, kind="sorted", lo=LO, hi=HI),
                    REPEATS)
        deg.append(t)
        print(f"{n:>8}{t:>12.5f}{t / n ** 2 * 1e8:>12.2f} (T/n² · 10⁸)")

    # Г4: максимальная глубина рекурсии
    sys.setrecursionlimit(20_000)
    print("\nГ4. Максимальная глубина рекурсии")
    print(f"{'n':>8}{'Тип':>5}{'Быстрая':>10}{'Быстрая (наивн.)':>18}"
          f"{'Слиянием':>10}{'log2 n':>9}")
    depth = {}
    for n in (3000, 50_000):
        for kind in ("random", "sorted", "reversed"):
            data = generate_data(n, kind=kind, lo=LO, hi=HI)
            naive = (quick_naive_depth(data)
                     if n <= 3000 or kind == "random" else None)
            depth[n, kind] = (quick_depth(data), naive, merge_depth(data))
            print(f"{n:>8}{KINDS[kind]:>5}{depth[n, kind][0]:>10}"
                  f"{naive if naive is not None else '—':>18}"
                  f"{depth[n, kind][2]:>10}{math.log2(n):>9.2f}")

    # Сводная таблица при n = 4500
    print("\nСводная таблица, n = 4500, случайные данные")
    base = res1["Пузырьком"][-1]
    for name, times in res1.items():
        print(f"{name:>12}{times[-1]:>10.5f} с  ускорение x{base / times[-1]:.0f}")

    # Графики
    fig, axes = plt.subplots(1, 3, figsize=(17, 5))
    for name, t in res1.items():
        axes[0].plot(small, t, marker="o", markersize=6, linewidth=2,
                     color=COLORS[name], label=name)
    axes[0].set_yscale("log")
    axes[0].set_xticks(small)
    axes[0].set_title("Эксперимент 1 (лог. шкала времени)")
    for name, t in res2.items():
        axes[1].plot(large, t, marker="o", markersize=6, linewidth=2,
                     color=COLORS[name], label=name)
        axes[1].annotate(f"{t[-1]:.3f} с", (large[-1], t[-1]),
                         textcoords="offset points", xytext=(-8, 6),
                         ha="right", fontsize=9, color="#333333")
    axes[1].set_xticks(large)
    axes[1].set_title("Эксперимент 2")
    for ax in axes[:2]:
        ax.set_xlabel("Размер массива n")
    width = 0.38
    xs = range(len(KINDS))
    for idx, (shift, name) in enumerate(((-width / 2, "Быстрая"),
                                         (width / 2, "Слиянием"))):
        vals = [res3[3000, kind][idx] for kind in KINDS]
        bars = axes[2].bar([x + shift for x in xs], vals, width * 0.95,
                           color=COLORS[name], label=name)
        axes[2].bar_label(bars, fmt="%.4f", fontsize=8, padding=2,
                          color="#333333")
    axes[2].set_xticks(list(xs), list(KINDS.values()))
    axes[2].set_xlabel("Тип данных (n = 3000)")
    axes[2].set_title("Эксперимент 3 (опорный — первый элемент)")
    for ax in axes:
        ax.set_ylabel("Время, с")
        ax.grid(True, color="#e5e5e5", linewidth=0.8)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.legend(frameon=False)
    axes[2].grid(False, axis="x")
    fig.tight_layout()
    fig.savefig("lr3_plot.png", dpi=150)
    plt.show()
