import sys
sys.path.insert(0, "/home/hoangvh1/Workspace/pyvinorm")  # Adjust path to import ViNormalizer

from pyvinorm import ViNormalizer
# from .. import tests
from tests.patterns import (
    test_address,
    test_datetime,
    test_math,
    test_special
)
import itertools
import time
import random
from multiprocessing import Pool, cpu_count
import statistics

normalizer = ViNormalizer()

def do_normalize(text):
    return normalizer.normalize(text)

def benchmark(corpus: list[str], n_tests: int = 1000):
    inputs = random.choices(corpus, k=n_tests)
    total_chars = sum(len(text) for text in inputs)
    print(f"Total characters in inputs: {total_chars}")

    duration = 0
    for inp in inputs:
        start = time.perf_counter()
        do_normalize(inp)
        end = time.perf_counter()
        duration += end - start
    
    cps = total_chars / duration if duration > 0 else 0
    print(f"Total duration: {duration:.2f} seconds")
    print(f"Characters per second: {cps:.2f}")
    return cps

def benchmark_mp(corpus: list[str], n_tests: int = 1000, n_proc: int = cpu_count()):
    inputs = random.choices(corpus, k=n_tests)
    total_chars = sum(len(text) for text in inputs)
    print(f"Total characters in inputs: {total_chars}")

    with Pool(n_proc) as pool:
        start = time.perf_counter()
        results = pool.map(do_normalize, inputs)
        end = time.perf_counter()

    duration = end - start
    cps = total_chars / duration if duration > 0 else 0
    print(f"Total duration: {duration:.2f} seconds")
    print(f"Characters per second: {cps:.2f}")
    return cps


if __name__ == "__main__":
    mp_benchmark = True  # Set to True to use multiprocessing
    corpus = itertools.chain(
        test_address.ADDRESS_PATTERNS,
        test_datetime.DATE_FROM_TO_TESTS,
        test_datetime.DATE_TESTS,
        test_datetime.TIME_TESTS,
        test_datetime.MONTH_TESTS,
        test_datetime.DATETIME_TESTS,
        test_math.DECIMAL_TESTS,
        test_math.MEASUREMENT_TESTS,
        test_math.ROMAN_TESTS,
        test_special.EMAIL_TESTS,
        test_special.FOOTBALL_PATTERNS,
        test_special.PHONE_NUMBER_TESTS,
        test_special.WEBSITE_TESTS
    )
    corpus = [test[0] for test in corpus]

    random.seed(42)  # For reproducibility
    n_runs = 100
    n_tests_per_run = 1000
    n_proc = 4

    cps_stats = []
    for _ in range(n_runs):
        print(f"Run {_ + 1}/{n_runs}")
        if mp_benchmark:
            cps = benchmark_mp(corpus, n_tests=n_tests_per_run, n_proc=n_proc)
        else:
            cps = benchmark(corpus, n_tests=n_tests_per_run)
        print(f"Run {_ + 1} - Characters per second: {cps:.2f}\n")

        cps_stats.append(cps)
    
    avg_cps = statistics.mean(cps_stats)
    std_cps = statistics.stdev(cps_stats)

    print("============================================")
    print(f"Average Characters per second: {avg_cps:.2f}")
    print(f"Standard Deviation: {std_cps:.2f}")
    print("============================================")
