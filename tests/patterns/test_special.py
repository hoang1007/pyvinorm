from typing import List
from pyvinorm import ViNormalizer


PHONE_NUMBER_TESTS = [
    (
        "Số điện thoại của tôi là +84 123 456 7890",
        "Số điện thoại của tôi là cộng tám bốn một hai ba bốn năm sáu bảy tám chín không",
    ),
    (
        "Liên hệ qua số 0123-456-789",
        "Liên hệ qua số không một hai ba - bốn năm sáu - bảy tám chín",
    ),
    (
        "Gọi cho tôi theo số +1.800.555.1234",
        "Gọi cho tôi theo số cộng một . tám không không . năm năm năm . một hai ba bốn",
    ),
    (
        "0 24 24 24 24",
        "không hai bốn hai bốn hai bốn hai bốn",
    ),
    (
        "+84 12 34 56 789",
        "cộng tám bốn một hai ba bốn năm sáu bảy tám chín",
    ),
    (
        "1900 1234",
        "một chín không không một hai ba bốn",
    ),
    (
        "1800.1090",
        "một tám không không . một không chín không",
    ),
    (
        "0908.144.144",
        "không chín không tám . một bốn bốn . một bốn bốn",
    ),
]

EMAIL_TESTS = [
    ("Email của tôi là abc@gmail.com", "Email của tôi là abc a còng gmail chấm com"),
    (
        "Liên hệ qua email: hoangvuhuy1007@gmail.com",
        "Liên hệ qua email : hoangvuhuy một không không bảy a còng gmail chấm com",
    ),
    ("cskh@thegioididong.com", "chăm sóc khách hàng a còng thế giới di động chấm com"),
    (
        "Hãy gửi email đến hòm thư: hoangvh@ppp.org",
        "Hãy gửi email đến hòm thư : hoangvh a còng ppp chấm o rờ gờ",
    ),
    (
        "Hãy gửi email đến hòm thư: hoangvh@x88.org.vn",
        "Hãy gửi email đến hòm thư : hoangvh a còng x tám tám chấm o rờ gờ chấm vi en",
    ),
]

WEBSITE_TESTS = [
    (
        "https://www.google.com",
        "hát tê tê pê ét hai chấm gạch chéo gạch chéo vê kép vê kép vê kép chấm google chấm com",
    ),
    (
        "https://vietnamnet.vn",
        "hát tê tê pê ét hai chấm gạch chéo gạch chéo vietnamnet chấm vi en",
    ),
    (
        "ftp://123.45.67.89:8080",
        "ép tê pê hai chấm gạch chéo gạch chéo một hai ba chấm bốn năm chấm sáu bảy chấm tám chín hai chấm tám không tám không",
    ),
]

FOOTBALL_PATTERNS = [
    ("Đội hình 3-4-3", "Đội hình ba bốn ba"),
    ("Đội hình 4-2-3-1", "Đội hình bốn hai ba một"),
    ("U12, U23, U.22", "U mười hai , U hai mươi ba , U hai mươi hai"),
    (
        "tỷ số 2 - 1 nghiêng về đội tuyển Việt Nam",
        "tỷ số hai một nghiêng về đội tuyển Việt Nam",
    ),
    (
        "Đội tuyển U23 Việt Nam đã giành chiến thắng với tỉ số 4-0",
        "Đội tuyển U hai mươi ba Việt Nam đã giành chiến thắng với tỉ số bốn không",
    ),
]


def assert_normalizing(pairs: List[tuple]):
    normalizer = ViNormalizer(downcase=False, keep_punctuation=True)

    for text, exp in pairs:
        assert normalizer.normalize(text) == exp


def test_phone_number_patterns():
    assert_normalizing(PHONE_NUMBER_TESTS)


def test_email_patterns():
    assert_normalizing(EMAIL_TESTS)


def test_website_patterns():
    assert_normalizing(WEBSITE_TESTS)


def test_football_patterns():
    assert_normalizing(FOOTBALL_PATTERNS)
