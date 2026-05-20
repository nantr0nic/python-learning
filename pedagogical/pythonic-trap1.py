import time


def time_func(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        wrapper.last_time: float = elapsed
        if elapsed < 1.0:
            print(f"  Time: {elapsed * 1000:.3f}ms")
        else:
            print(f"  Time: {elapsed:.3f}s")
        return result

    return wrapper


@time_func
def count_pos_sum_neg_pythonic(array: list) -> list:
    if array is None or len(array) == 0:
        return []

    pos_count: int = sum(1 for x in array if x > 0)
    neg_sum: int = sum(x for x in array if x < 0)

    return [pos_count, neg_sum]


@time_func
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

    print("=== Benchmarking single vs double iteration ===\n")

    for size in sizes:
        arr = arrays[size]
        print(f"--- Array size: {size:,} ---")

        result_single = count_pos_sum_neg(arr)
        result_double = count_pos_sum_neg_pythonic(arr)

        diff = count_pos_sum_neg_pythonic.last_time - count_pos_sum_neg.last_time
        if diff >= 0:
            if diff < 1.0:
                print(f"  Double was {diff * 1000:.3f}ms slower")
            else:
                print(f"  Double was {diff:.3f}s slower")
        else:
            if -diff < 1.0:
                print(f"  Double was {-diff * 1000:.3f}ms faster")
            else:
                print(f"  Double was {-diff:.3f}s faster")

        print(f"  Results -> single: {result_single}, double: {result_double}\n")


if __name__ == "__main__":
    main()
