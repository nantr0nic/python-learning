import time

RUNS = 5


def count_pos_sum_neg_pythonic(array: list) -> list:
    if array is None or len(array) == 0:
        return []

    pos_count: int = sum(1 for x in array if x > 0)
    neg_sum: int = sum(x for x in array if x < 0)

    return [pos_count, neg_sum]


def count_pos_sum_neg(array: list) -> list:
    if array is None or len(array) == 0:
        return []

    pos_count: int = 0
    neg_sum: int = 0

    for x in array:
        if x > 0:
            pos_count += 1
        elif x < 0:
            neg_sum += x

    return [pos_count, neg_sum]


def main():
    sizes = [100, 1000, 10000, 100000, 1000000, 100000000, 500000000]
    arrays = {
        100: [i for i in range(-50, 50)],
        1000: [i for i in range(-500, 500)],
        10000: [i for i in range(-5000, 5000)],
        100000: [i for i in range(-50000, 50000)],
        1000000: [i for i in range(-500000, 500000)],
        100000000: [i for i in range(-5000000, 5000000)],
        500000000: [i for i in range(-250000000, 250000000)],
    }

    print(f"=== Average over {RUNS} runs ===\n")

    for size in sizes:
        arr = arrays[size]
        times_single = []
        times_double = []

        for run in range(1, RUNS + 1):
            start = time.perf_counter()
            result_single = count_pos_sum_neg(arr)
            times_single.append(time.perf_counter() - start)

            start = time.perf_counter()
            result_double = count_pos_sum_neg_pythonic(arr)
            times_double.append(time.perf_counter() - start)

        avg_single = sum(times_single) / RUNS
        avg_double = sum(times_double) / RUNS
        diff = avg_double - avg_single

        print(f"--- Array size: {size:,} ---")
        if avg_single < 1.0:
            print(f"  Single iteration (avg): {avg_single * 1000:.3f}ms")
        else:
            print(f"  Single iteration (avg): {avg_single:.3f}s")
        if avg_double < 1.0:
            print(f"  Double iteration (avg): {avg_double * 1000:.3f}ms")
        else:
            print(f"  Double iteration (avg): {avg_double:.3f}s")

        if diff >= 0:
            unit = "ms" if diff < 1.0 else "s"
            value = diff * 1000 if diff < 1.0 else diff
            print(f"  Double was {value:.3f}{unit} slower on average")
        else:
            unit = "ms" if -diff < 1.0 else "s"
            value = -diff * 1000 if -diff < 1.0 else -diff
            print(f"  Double was {value:.3f}{unit} faster on average")

        print(f"  Results -> {result_single}\n")


if __name__ == "__main__":
    main()
