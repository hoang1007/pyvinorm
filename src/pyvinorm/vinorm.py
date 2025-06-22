import logging

import regex
from pyvinorm.patterns.handler import PatternHandler
from pyvinorm.managers import MappingManager, init_resources
from pyvinorm.utils.string_utils import (
    remove_white_space,
    replace_nonvoice_symbols,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ViNormalizer:
    """Vietnamese text normalizer that convert text to its spoken form.

    :param bool regex_only: If True, only applies regex patterns without further normalization.
    :param bool keep_punctuation: If True, do not replace punctuation with dot or comma.
    :param bool downcase: If True, converts the text to lowercase after normalization.

    :return str: Normalized text in spoken form.
    """

    def __init__(
        self,
        regex_only: bool = False,
        keep_punctuation: bool = False,
        downcase: bool = True,
    ):
        self.regex_only = regex_only
        self.keep_punctuation = keep_punctuation
        self.downcase = downcase

        init_resources()

        self.pattern_handler = PatternHandler()

    def normalize(self, text: str) -> str:
        """
        Normalize the input text using defined patterns and mappings.
        """
        acronym_mapping = MappingManager.get_mapping("Acronyms")
        teencode_mapping = MappingManager.get_mapping("Teencode")
        symbol_mapping = MappingManager.get_mapping("Symbol")

        normalized_text = remove_white_space(text)

        # Step 1: Normalize text using regex patterns
        normalized_text = self.pattern_handler.normalize(normalized_text)

        if self.regex_only:
            normalized_text = remove_white_space(normalized_text)
            return normalized_text

        # Step 2: Check whether normalized text still contains parts
        # that aren't converted to spoken forms.
        normalized_text = replace_nonvoice_symbols(normalized_text, repl="")
        symbol_pattern = regex.compile(r"[^\w\d\s]")
        normalized_text = symbol_pattern.sub(
            lambda m: " " + m.group() + " ", normalized_text
        )

        result = ""
        for token in normalized_text.split():
            token_lower = token.lower()
            if acronym_mapping.contains(token_lower):
                result += " " + acronym_mapping.get_with_context(token_lower, result, token_lower)
            elif teencode_mapping.contains(token_lower):
                result += " " + teencode_mapping.get_with_context(token_lower, result, token_lower)
            elif symbol_mapping.contains(token):
                result += " " + symbol_mapping.get(token)
            elif token in (".", "!", ":", "?"):
                result += " " + (token if self.keep_punctuation else ".")
            elif token in (",", ";", "/", "-"):
                result += " " + (token if self.keep_punctuation else ",")
            else:
                result += " " + token

        # Step 3: Postprocess the result
        result = remove_white_space(result.lstrip())

        if self.downcase:
            result = result.lower()

        return result
