"""
Лабораторная работа № 3. Вариант 0.
Быстрая сортировка (Хоар, средний опорный) и сортировка слиянием.
Сравнение с алгоритмами ЛР № 2 и встроенной sorted().
"""
import math
import sys
from pathlib import Path

# модули sorts_common.py и lr2.py лежат в папке ЛР № 2
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lab2"))

from sorts_common import generate_data, measure  # noqa: E402
from lr2 import bubble_sort, insertion_sort      # noqa: E402


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
    """Разбиение Хоара, опорный элемент — средний."""
    pivot = a[(lo + hi) // 2]
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


# ---------- Эксперименты ----------
def run_experiment(algorithms, sizes, kind="random", repeats=3):
    results = {name: [] for name in algorithms}
    print(f"{'n':>8}" + "".join(f"{name:>12}" for name in algorithms))
    for n in sizes:
        data = generate_data(n, kind=kind)
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

    # Эксперимент 1: четыре алгоритма
    print("Эксперимент 1: четыре алгоритма, случайные данные")
    small = [500, 1000, 2000, 3000, 4000, 5000]
    res1 = run_experiment({"Пузырьком": bubble_sort,
                           "Вставками": insertion_sort,
                           "Быстрая": quick_sort,
                           "Слиянием": merge_sort}, small)

    # Эксперимент 2: O(n log n) на больших размерах
    print("\nЭксперимент 2: алгоритмы O(n log n) на больших массивах")
    large = [10_000, 25_000, 50_000, 100_000, 200_000]
    res2 = run_experiment({"Быстрая": quick_sort,
                           "Слиянием": merge_sort,
                           "sorted()": sorted}, large)
    print(f"\n{'n':>8}{'Слиянием / Быстрая':>22}{'Быстрая / sorted()':>22}")
    for k, n in enumerate(large):
        print(f"{n:>8}{res2['Слиянием'][k] / res2['Быстрая'][k]:>22.2f}"
              f"{res2['Быстрая'][k] / res2['sorted()'][k]:>22.2f}")

    # Проверка роста T(2n)/T(n)
    print("\nОтношение T(2n)/T(n)")
    print(f"{'Переход':>18}{'Быстрая':>10}{'Слиянием':>10}"
          f"{'n log n':>10}{'n²':>6}")
    for n in large:
        if 2 * n in large:
            i, j = large.index(n), large.index(2 * n)
            theory = 2 * math.log(2 * n) / math.log(n)
            print(f"{n:>8} -> {2 * n:<7}"
                  f"{res2['Быстрая'][j] / res2['Быстрая'][i]:>10.2f}"
                  f"{res2['Слиянием'][j] / res2['Слиянием'][i]:>10.2f}"
                  f"{theory:>10.2f}{4:>6}")

    # Эксперимент 3: влияние структуры данных
    print("\nЭксперимент 3, n = 50 000")
    kinds = {"random": "R", "sorted": "S", "reversed": "V",
             "nearly_sorted": "N", "duplicates": "D"}
    res3 = {"Быстрая": [], "Слиянием": []}
    for kind in kinds:
        data = generate_data(50_000, kind=kind)
        tq, tm = measure(quick_sort, data), measure(merge_sort, data)
        res3["Быстрая"].append(tq)
        res3["Слиянием"].append(tm)
        print(f"{kind:>15} ({kinds[kind]}): быстрая {tq:.5f} с, "
              f"слиянием {tm:.5f} с")

    # Сводная таблица при n = 5000
    print("\nСводная таблица, n = 5000, случайные данные")
    base = res1["Пузырьком"][-1]
    for name, times in res1.items():
        print(f"{name:>12}{times[-1]:>10.5f} с  ускорение x{base / times[-1]:.0f}")

    # Графики
    fig, axes = plt.subplots(1, 3, figsize=(17, 5))
    for name, t in res1.items():
        axes[0].plot(small, t, marker="o", markersize=6, linewidth=2,
                     color=COLORS[name], label=name)
    axes[0].set_yscale("log")
    axes[0].set_title("Эксперимент 1 (лог. шкала времени)")
    for name, t in res2.items():
        axes[1].plot(large, t, marker="o", markersize=6, linewidth=2,
                     color=COLORS[name], label=name)
        axes[1].annotate(f"{t[-1]:.3f} с", (large[-1], t[-1]),
                         textcoords="offset points", xytext=(-8, 6),
                         ha="right", fontsize=9, color="#333333")
    axes[1].set_title("Эксперимент 2")
    for ax in axes[:2]:
        ax.set_xlabel("Размер массива n")
    width = 0.38
    xs = range(len(kinds))
    for shift, name in ((-width / 2, "Быстрая"), (width / 2, "Слиянием")):
        bars = axes[2].bar([x + shift for x in xs], res3[name], width * 0.95,
                           color=COLORS[name], label=name)
        axes[2].bar_label(bars, fmt="%.3f", fontsize=8, padding=2,
                          color="#333333")
    axes[2].set_xticks(list(xs), list(kinds.values()))
    axes[2].set_xlabel("Тип данных (n = 50 000)")
    axes[2].set_title("Эксперимент 3")
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
