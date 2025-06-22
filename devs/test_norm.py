from pyvinorm import ViNormalizer


if __name__ == "__main__":
    normalizer = ViNormalizer()

    # print(normalizer.normalize("vk ck son"))
    print(normalizer.normalize("vòng ck vk ck son"))
    print(normalizer.normalize("thị trường ck đang nóng 24/7"))