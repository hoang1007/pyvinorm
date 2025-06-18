from typing import List
from pyvinorm import ViNormalizer


DECIMAL_TESTS = [
    ("1.234,56", "một nghìn hai trăm ba mươi tư phẩy năm sáu"),
    ("12.345,67", "mười hai nghìn ba trăm bốn mươi lăm phẩy sáu bảy"),
    ("123.456,78", "một trăm hai mươi ba nghìn bốn trăm năm mươi sáu phẩy bảy tám"),
    ("1.234,56", "một nghìn hai trăm ba mươi tư phẩy năm sáu"),
    (
        "1.409.234,5680",
        "một triệu bốn trăm linh chín nghìn hai trăm ba mươi tư phẩy năm sáu tám không",
    ),
    ("1,234,567", "một triệu hai trăm ba mươi tư nghìn năm trăm sáu mươi bảy"),
    ("1,123.56", "một nghìn một trăm hai mươi ba phẩy năm sáu"),
    ("-1.234,56", "âm một nghìn hai trăm ba mươi tư phẩy năm sáu"),
]

ROMAN_TESTS = [
    ("đại hội Đại biểu lần thứ XXVI", "đại hội Đại biểu lần thứ hai mươi sáu"),
    ("thế kỷ XXI", "thế kỷ hai mươi mốt"),
    ("lần thứ IV", "lần thứ bốn"),
    ("kỳ họp thứ IX", "kỳ họp thứ chín"),
]

MEASUREMENT_TESTS = [
    ("40°C", "bốn mươi độ xê"),
    ("40.1cm", "bốn mươi phẩy một xăng ti mét"),
    ("40.1cm2", "bốn mươi phẩy một xăng ti mét vuông"),
    ("1.234,56km3", "một nghìn hai trăm ba mươi tư phẩy năm sáu ki lô mét khối"),
    ("2,342.08ha", "hai nghìn ba trăm bốn mươi hai phẩy không tám héc ta"),
]


def assert_normalizing(pairs: List[tuple]):
    normalizer = ViNormalizer(downcase=False, keep_punctuation=True)

    for text, exp in pairs:
        assert normalizer.normalize(text) == exp


def test_decimal_patterns():
    assert_normalizing(DECIMAL_TESTS)


def test_roman_patterns():
    assert_normalizing(ROMAN_TESTS)


def test_measurement_patterns():
    assert_normalizing(MEASUREMENT_TESTS)
