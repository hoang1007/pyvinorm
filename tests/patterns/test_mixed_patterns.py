from typing import List
import random

from pyvinorm import ViNormalizer

import test_address
import test_datetime
import test_math
import test_special


TEST_CORPUS = [
    test_address.ADDRESS_PATTERNS,
    test_datetime.DATE_TESTS,
    test_datetime.DATE_FROM_TO_TESTS,
    test_datetime.MONTH_TESTS,
    test_datetime.DATETIME_TESTS,
    test_math.DECIMAL_TESTS,
    test_math.ROMAN_TESTS,
    test_math.MEASUREMENT_TESTS,
    test_special.PHONE_NUMBER_TESTS,
    test_special.EMAIL_TESTS,
    test_special.WEBSITE_TESTS,
    test_special.FOOTBALL_PATTERNS,
]


def generate_testcases(n: int, seed: int = 42):
    random.seed(seed)
    test_cases = []

    for _ in range(n):
        test_case = []
        n_test_type = random.randint(1, len(TEST_CORPUS))
        selected_indices = random.sample(range(len(TEST_CORPUS)), n_test_type)
        for idx in selected_indices:
            test_case.append(random.choice(TEST_CORPUS[idx]))
        
        text = " ? ".join([pair[0] for pair in test_case])
        expected = " ? ".join([pair[1] for pair in test_case])
        test_cases.append((text, expected))

    return test_cases

def assert_normalizing(text, expected):
    normalizer = ViNormalizer(downcase=False, keep_punctuation=True)

    assert normalizer.normalize(text) == expected

def test_mixed_patterns():
    test_cases = generate_testcases(n=100, seed=42)
    for text, expected in test_cases:
        assert_normalizing(text, expected)
        # Uncomment the line below to print the test case
        # print(f"Text: {text} | Expected: {expected}")
