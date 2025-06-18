from typing import List
from pyvinorm import ViNormalizer

TIME_TESTS = [
    ("bây giờ là 10 h30am", "bây giờ là mười giờ ba mươi ây em"),
    (
        "bây giờ là 19h tèo teo téo teo tèo teo tèo",
        "bây giờ là mười chín giờ tèo teo téo teo tèo teo tèo",
    ),
    ("23h", "hai mươi ba giờ"),
    ("24g", "hai mươi tư giờ"),
    ("09:30", "chín giờ ba mươi"),
    ("9h2m2s", "chín giờ hai phút hai giây"),
    ("9:45", "chín giờ bốn mươi lăm"),
    ("21g26p", "hai mươi mốt giờ hai mươi sáu phút"),
    ("01:20:30", "một giờ hai mươi phút ba mươi giây"),
    ("23h24m45s", "hai mươi ba giờ hai mươi tư phút bốn mươi lăm giây"),
    ("9h - 10h", "chín giờ đến mười giờ"),
    ("9h20p- 10h30", "chín giờ hai mươi phút đến mười giờ ba mươi"),
    ("9h2p - 9h5p", "chín giờ hai phút đến chín giờ năm phút"),
    ("12h24p30s", "mười hai giờ hai mươi tư phút ba mươi giây"),
]


DATE_TESTS = [
    ("ngày 10/3/2025", "ngày mười tháng ba năm hai nghìn không trăm hai mươi lăm"),
    ("02/9/1945", "hai tháng chín năm một nghìn chín trăm bốn mươi lăm"),
    ("5-09-1890", "năm tháng chín năm một nghìn tám trăm chín mươi"),
    ("20.6.2025", "hai mươi tháng sáu năm hai nghìn không trăm hai mươi lăm"),
    ("24 - 7 - 2002", "hai mươi tư tháng bảy năm hai nghìn không trăm linh hai"),
]

DATE_FROM_TO_TESTS = [
    ("từ 20/4 đến 30/6", "từ hai mươi tháng tư đến ba mươi tháng sáu"),
    (
        "từ 01/2025 đến 12/2025",
        "từ tháng một năm hai nghìn không trăm hai mươi lăm đến tháng mười hai năm hai nghìn không trăm hai mươi lăm",
    ),
    (
        "từ 02/2023 - 11/2024",
        "từ tháng hai năm hai nghìn không trăm hai mươi ba đến tháng mười một năm hai nghìn không trăm hai mươi tư",
    ),
    ("từ 20-30/4", "từ hai mươi đến ba mươi tháng tư"),
    (
        "từ 01-12/2025",
        "từ tháng một đến tháng mười hai năm hai nghìn không trăm hai mươi lăm",
    ),
    (
        "từ 02/2023 đến tháng 11/2024",
        "từ tháng hai năm hai nghìn không trăm hai mươi ba đến tháng mười một năm hai nghìn không trăm hai mươi tư",
    ),
]

MONTH_TESTS = [
    ("tháng 01/2025", "tháng một năm hai nghìn không trăm hai mươi lăm"),
    ("tháng 10/1998", "tháng mười năm một nghìn chín trăm chín mươi tám"),
    ("tháng 12/2024", "tháng mười hai năm hai nghìn không trăm hai mươi tư"),
    ("tháng 02/2023", "tháng hai năm hai nghìn không trăm hai mươi ba"),
    ("tháng 11/2024", "tháng mười một năm hai nghìn không trăm hai mươi tư"),
]

DATETIME_TESTS = [
    ("sáng mùng 8/3", "sáng mùng tám tháng ba"),
    ("đêm 29-12", "đêm hai mươi chín tháng mười hai"),
    ("rạng sáng 30/04", "rạng sáng ba mươi tháng tư"),
]


def assert_normalizing(pairs: List[tuple]):
    normalizer = ViNormalizer(downcase=False, keep_punctuation=True)

    for text, exp in pairs:
        assert normalizer.normalize(text) == exp


def test_time_patterns():
    assert_normalizing(DATETIME_TESTS)


def test_date_patterns():
    assert_normalizing(DATE_TESTS)


def test_date_from_to_patterns():
    assert_normalizing(DATE_FROM_TO_TESTS)


def test_month_patterns():
    assert_normalizing(MONTH_TESTS)


def test_datetime_patterns():
    assert_normalizing(DATETIME_TESTS)
