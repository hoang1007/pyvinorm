from typing import List
from pyvinorm import ViNormalizer


ADDRESS_PATTERNS = [
    (
        "Số nhà 123, đường Nguyễn Văn Cừ, quận 1",
        "Số nhà một trăm hai mươi ba , đường Nguyễn Văn Cừ , quận một",
    ),
    (
        "Đường Trần Hưng Đạo, phường Bến Thành, quận 1",
        "Đường Trần Hưng Đạo , phường Bến Thành , quận một",
    ),
    (
        "Số nhà 456, khu phố 5, thị trấn Thạnh Mỹ Lợi, huyện Nhà Bè",
        "Số nhà bốn trăm năm mươi sáu , khu phố năm , thị trấn Thạnh Mỹ Lợi , huyện Nhà Bè",
    ),
    (
        "Số nhà 789, đường Lê Lợi, tp. Hồ Chí Minh, mã bưu chính 700000",
        "Số nhà bảy trăm tám mươi chín , đường Lê Lợi , thành phố Hồ Chí Minh , mã bưu chính bảy không không không không không",
    ),
    (
        "Số nhà 101-102A, đường Nguyễn Thị Minh Khai (gần chợ Bến Thành)",
        "Số nhà một trăm linh một - một trăm linh hai A , đường Nguyễn Thị Minh Khai gần chợ Bến Thành",
    ),
    (
        "số 202, Dịch Vọng, q.Cầu Giấy, tp.Hà Nội",
        "số hai trăm linh hai , Dịch Vọng , quận Cầu Giấy , thành phố Hà Nội",
    ),
    (
        "phòng 301, tòa nhà Vincom Center, 171 Đường Đồng Khởi, quận 1",
        "phòng ba trăm linh một , tòa nhà Vincom Center , một trăm bảy mươi mốt Đường Đồng Khởi , quận một",
    ),
    (
        "lớp 6A1, trường THCS Nguyễn Du, 123 Đường Lê Lai, phường Bến Nghé, quận 1",
        "lớp sáu A một , trường trung học cơ sở Nguyễn Du , một trăm hai mươi ba Đường Lê Lai , phường Bến Nghé , quận một",
    ),
    (
        "kp. 4, phường Tân Hưng Thuận, quận 12, tp.HCM",
        "khu phố bốn , phường Tân Hưng Thuận , quận mười hai , thành phố hồ chí minh",
    ),
    (
        "p. Dịch Vọng Hậu, quận Cầu Giấy, tp. Hà Nội",
        "phường Dịch Vọng Hậu , quận Cầu Giấy , thành phố Hà Nội",
    ),
    (
        "h. Kim Sơn, tỉnh Ninh Bình, Việt Nam",
        "huyện Kim Sơn , tỉnh Ninh Bình , Việt Nam",
    ),
    (
        "tx. Tân Uyên, tỉnh Bình Dương, Việt Nam",
        "thị xã Tân Uyên , tỉnh Bình Dương , Việt Nam",
    ),
    (
        "x. Phú Mỹ, h. Tân Thành, t . Bà Rịa - Vũng Tàu",
        "xã Phú Mỹ , huyện Tân Thành , tỉnh Bà Rịa - Vũng Tàu",
    ),
    (
        "khu đô thị mới Thủ Thiêm, phường An Khánh, quận 2, tp.HCM",
        "khu đô thị mới Thủ Thiêm , phường An Khánh , quận hai , thành phố hồ chí minh",
    )
]


def assert_normalizing(pairs: List[tuple]):
    normalizer = ViNormalizer(downcase=False, keep_punctuation=True)

    for text, exp in pairs:
        assert normalizer.normalize(text) == exp


def test_address_patterns():
    assert_normalizing(ADDRESS_PATTERNS)
