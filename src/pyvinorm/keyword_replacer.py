# Keyword replacement module
# Time complexity: O(N), where N is the number of characters in the input text

from typing import Dict
from flashtext import KeywordProcessor


class KeywordReplacer:
    def __init__(self, keyword_mapping: Dict[str, str], case_sensitive: bool = False):
        self.processor = KeywordProcessor(case_sensitive=case_sensitive)

        for key, repl in keyword_mapping.items():
            self.processor.add_keyword(key, repl)

    def __call__(self, text: str):
        return self.processor.replace_keywords(text)
