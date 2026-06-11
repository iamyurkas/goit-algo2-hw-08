from collections import OrderedDict
import random
import time


class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1

        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


def range_sum_no_cache(array, left, right):
    return sum(array[left:right + 1])


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, left, right, cache):
    key = (left, right)

    cached_result = cache.get(key)
    if cached_result != -1:
        return cached_result

    result = sum(array[left:right + 1])
    cache.put(key, result)

    return result


def update_with_cache(array, index, value, cache):
    array[index] = value

    for key in list(cache.cache.keys()):
        left, right = key
        if left <= index <= right:
            del cache.cache[key]


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [
        (random.randint(0, n // 2), random.randint(n // 2, n - 1))
        for _ in range(hot_pool)
    ]

    queries = []

    for _ in range(q):
        if random.random() < p_update:
            index = random.randint(0, n - 1)
            value = random.randint(1, 100)
            queries.append(("Update", index, value))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)

            queries.append(("Range", left, right))

    return queries


def run_no_cache(array, queries):
    arr = array.copy()

    start = time.perf_counter()

    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(arr, query[1], query[2])
        elif query[0] == "Update":
            update_no_cache(arr, query[1], query[2])

    return time.perf_counter() - start


def run_with_cache(array, queries):
    arr = array.copy()
    cache = LRUCache(1000)

    start = time.perf_counter()

    for query in queries:
        if query[0] == "Range":
            range_sum_with_cache(arr, query[1], query[2], cache)
        elif query[0] == "Update":
            update_with_cache(arr, query[1], query[2], cache)

    return time.perf_counter() - start


def main():
    random.seed(42)

    n = 100_000
    q = 50_000

    array = [random.randint(1, 100) for _ in range(n)]
    queries = make_queries(n, q)

    time_no_cache = run_no_cache(array, queries)
    time_with_cache = run_with_cache(array, queries)

    speedup = time_no_cache / time_with_cache

    print(f"Без кешу : {time_no_cache:.2f} с")
    print(f"LRU-кеш  : {time_with_cache:.2f} с  (прискорення ×{speedup:.2f})")


if __name__ == "__main__":
    main()
