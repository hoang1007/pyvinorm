import logging

from typing import List, Dict, Sequence, Union, Callable
import regex

from .base import BasePattern
from .registry import get_patterns


logger = logging.getLogger(__name__)


class PatternHandler:
    def __init__(self):
        self.patterns = get_patterns()
        # Sort patterns by priority from highest to lowest
        self.patterns = {
            pattern_id: pattern
            for pattern_id, pattern in sorted(
                self.patterns.items(),
                key=lambda item: item[1].get_priority(),
                reverse=True,
            )
        }
        self.pattern_tags = set()
        for pattern in self.patterns.values():
            self.pattern_tags.update(pattern.tags)

    def _normalize(self, text: str, pattern: BasePattern):
        regex_pattern = regex.compile(pattern.get_regex_pattern())

        last_pos = 0
        result = ""
        for matcher in regex_pattern.finditer(text):
            start, end = matcher.span()
            result += text[last_pos:start]
            try:
                repl = pattern.handle_match(matcher) + " "
            except Exception as e:
                logger.error(f"Error handling match for pattern {pattern.__class__.__name__}: {e}")
                repl = matcher.group()  # Fallback to original match if error occurs
            result += repl
            last_pos = end
        result += text[last_pos:]
        return result

    def normalize(self, text: str, tag: str) -> str:
        """
        Normalize the text to a standard format.
        """
        if tag not in self.pattern_tags:
            raise ValueError(
                f"Tag '{tag}' is not valid. Available tags: {self.pattern_tags}"
            )

        if tag == "default":
            patterns_to_apply = {
                pattern_id: pattern
                for pattern_id, pattern in self.patterns.items()
                if pattern.is_enabled_by_default()
            }
        else:
            patterns_to_apply = {
                pattern_id: pattern
                for pattern_id, pattern in self.patterns.items()
                if tag in pattern.tags
            }

        result = text

        for pattern_id, pattern in patterns_to_apply.items():
            result = self._normalize(result, pattern)

        return result
