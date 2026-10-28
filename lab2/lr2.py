"""
Лабораторная работа № 2. Вариант 16.
Сравнение сортировки пузырьком и сортировки вставками.
Доп. задание М3: сортировка по убыванию через параметр reverse.
"""
import operator

from sorts_common import generate_data, measure

LO, HI = 0, 1_000_000             # диапазон значений варианта


def bubble_sort(arr, reverse=False):
    """Сортировка пузырьком с флагом досрочного выхода.

    reverse=False — по возрастанию, reverse=True — по убыванию."""
    out_of_order = operator.lt if reverse else operator.gt
    a = arr.copy()
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if out_of_order(a[j], a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def insertion_sort(arr, reverse=False):
    """Сортировка вставками.

    reverse=False — по возрастанию, reverse=True — по убыванию."""
    out_of_order = operator.lt if reverse else operator.gt
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and out_of_order(a[j], key):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    SIZES = [500, 1500, 2500, 3500, 4500]
    REPEATS = 3
    algorithms = {"Пузырьком": bubble_sort, "Вставками": insertion_sort}
    colors = {"Пузырьком": "#2a78d6", "Вставками": "#eb6834"}

    # М3: демонстрация на коротком массиве
    demo = generate_data(10, lo=LO, hi=HI)
    print("Исходный массив:     ", demo)
    for name, func in algorithms.items():
        print(f"{name:<10} возр.:  ", func(demo))
        print(f"{name:<10} убыв.:  ", func(demo, reverse=True))
    print()

    results = {(name, rev): [] for name in algorithms for rev in (False, True)}
    print(f"{'n':>6}" + "".join(f"{name + ' ↑':>14}{name + ' ↓':>14}"
                                for name in algorithms) + f"{'Пуз./Вст.':>12}")
    for n in SIZES:
        data = generate_data(n, kind="random", lo=LO, hi=HI)
        row = f"{n:>6}"
        for name, func in algorithms.items():
            for rev in (False, True):
                t = measure(func, data, REPEATS, reverse=rev)
                results[name, rev].append(t)
                row += f"{t:>14.4f}"
        row += (f"{results['Пузырьком', False][-1]
                   / results['Вставками', False][-1]:>12.2f}")
        print(row)

    # Проверка квадратичного роста: T(n2)/T(n1) против (n2/n1)²
    print("\nОтношение T(n2)/T(n1) (по возрастанию), теория для Θ(n²): (n2/n1)²")
    for n1, n2 in zip(SIZES, SIZES[1:]):
        i, j = SIZES.index(n1), SIZES.index(n2)
        print(f"{n1:>6} -> {n2:<6}" + "".join(
            f"{results[name, False][j] / results[name, False][i]:>14.2f}"
            for name in algorithms) + f"{(n2 / n1) ** 2:>14.2f}")

    print("\nОтношение T(n)/n² · 10⁸ (должно быть примерно постоянным)")
    for k, n in enumerate(SIZES):
        print(f"{n:>6}" + "".join(
            f"{results[name, rev][k] / n ** 2 * 1e8:>14.2f}"
            for name in algorithms for rev in (False, True)))

    print("\nМ3. Отношение T(убыв.)/T(возр.)")
    for k, n in enumerate(SIZES):
        print(f"{n:>6}" + "".join(
            f"{results[name, True][k] / results[name, False][k]:>14.2f}"
            for name in algorithms))

    fig, ax = plt.subplots(figsize=(8, 5))
    for (name, rev), times in results.items():
        ax.plot(SIZES, times, marker="o", markersize=6, linewidth=2,
                color=colors[name], linestyle="--" if rev else "-",
                label=f"{name}, по {'убыванию' if rev else 'возрастанию'}")
    for name in algorithms:
        t = results[name, False][-1]
        ax.annotate(f"{t:.3f} с", (SIZES[-1], t),
                    textcoords="offset points", xytext=(-8, 8),
                    ha="right", fontsize=9, color="#333333")
    ax.set_xlabel("Размер массива n")
    ax.set_ylabel("Время, с")
    ax.set_title("Зависимость времени сортировки от n (случайные данные)")
    ax.set_xticks(SIZES)
    ax.grid(True, color="#e5e5e5", linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig("lr2_plot.png", dpi=150)
    plt.show()
