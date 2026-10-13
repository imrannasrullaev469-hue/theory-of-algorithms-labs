"""
Лабораторная работа № 2. Вариант 0.
Сравнение сортировки пузырьком и сортировки вставками.
"""
from sorts_common import generate_data, measure


def bubble_sort(arr):
    """Сортировка пузырьком с флагом досрочного выхода."""
    a = arr.copy()
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def insertion_sort(arr):
    """Сортировка вставками."""
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    SIZES = [500, 1000, 2000, 3000, 4000, 5000]
    REPEATS = 3
    algorithms = {"Пузырьком": bubble_sort, "Вставками": insertion_sort}
    colors = {"Пузырьком": "#2a78d6", "Вставками": "#eb6834"}
    results = {name: [] for name in algorithms}

    print(f"{'n':>6}" + "".join(f"{name:>14}" for name in algorithms)
          + f"{'Пуз./Вст.':>12}")
    for n in SIZES:
        data = generate_data(n, kind="random")
        row = f"{n:>6}"
        for name, func in algorithms.items():
            t = measure(func, data, REPEATS)
            results[name].append(t)
            row += f"{t:>14.4f}"
        row += f"{results['Пузырьком'][-1] / results['Вставками'][-1]:>12.2f}"
        print(row)

    # Проверка квадратичного роста
    print("\nОтношение T(2n)/T(n), теория для Θ(n²): 4")
    for n in SIZES:
        if 2 * n in SIZES:
            i, j = SIZES.index(n), SIZES.index(2 * n)
            print(f"{n:>6} -> {2 * n:<6}" + "".join(
                f"{results[name][j] / results[name][i]:>14.2f}" for name in algorithms))

    print("\nОтношение T(n)/n² · 10⁸ (должно быть примерно постоянным)")
    for k, n in enumerate(SIZES):
        print(f"{n:>6}" + "".join(
            f"{results[name][k] / n ** 2 * 1e8:>14.2f}" for name in algorithms))

    fig, ax = plt.subplots(figsize=(8, 5))
    for name, times in results.items():
        ax.plot(SIZES, times, marker="o", markersize=6, linewidth=2,
                color=colors[name], label=name)
        ax.annotate(f"{times[-1]:.3f} с", (SIZES[-1], times[-1]),
                    textcoords="offset points", xytext=(-8, 8),
                    ha="right", fontsize=9, color="#333333")
    ax.set_xlabel("Размер массива n")
    ax.set_ylabel("Время, с")
    ax.set_title("Зависимость времени сортировки от n (случайные данные)")
    ax.grid(True, color="#e5e5e5", linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig("lr2_plot.png", dpi=150)
    plt.show()
