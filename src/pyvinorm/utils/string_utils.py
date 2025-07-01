import re
import regex
import string
from pyvinorm.managers import Mapping


def remove_white_space(text: str) -> str:
    """
    Remove extra white spaces from the text.
    """
    return " ".join(text.split())


def replace_nonvoice_symbols(text: str, repl: str = "") -> str:
    """
    Remove non-voice symbols from the text.
    """
    # Define a regex pattern to match non-voice symbols
    pattern = re.compile(r"(“|”|\.\.\.|\"|\'|\{|\}|\[|\]|\(|\))")
    return pattern.sub(repl, text)


VI_LETTERS = "aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ"


def is_valid(text: str) -> bool:
    """
    Whether input text is a valid text.

    A valid text is a text that does not empty and only contains
    Vietnamese letters, digits, spaces, and some punctuation marks.
    """
    pattern = regex.compile(f"^[{VI_LETTERS}0-9\\s{regex.escape(string.punctuation)}]+$")
    return (pattern.fullmatch(text) is not None) and (len(text) > 0)


# def contain_only_letters(text: str, letter_mapping: Mapping) -> bool:
#     for c in text.lower():
#         if not letter_mapping.contains(c):
#             return False
#     return True


# def read_letter_by_letter(text: str, lettersound_mapping: Mapping) -> str:
#     """
#     Read the text letter by letter using the provided lettersound mapping.
#     """
#     result = ""
#     for char in text.lower():
#         if lettersound_mapping.contains(char):
#             result += " " + lettersound_mapping.get(char, char)
#     return result.lstrip()
