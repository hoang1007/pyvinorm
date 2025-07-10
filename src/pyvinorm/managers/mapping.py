import logging

from typing import Dict, Optional, Tuple
from threading import Lock, Thread
from .lm import LanguageModelManager

logger = logging.getLogger(__name__)


class Mapping:

    @staticmethod
    def from_file(file_path: str, delimiter: str = "#") -> "Mapping":
        """
        Load mappings from a file.

        :param file_path: Path to the file containing mappings.
        :return: An instance of Mapping with loaded data.
        """
        mapping = Mapping()
        mapping.__map = {}
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                key, value = line.strip().split(delimiter)
                if key in mapping.__map:
                    mapping.__map[key] += (value,)
                else:
                    mapping.__map[key] = (value,)
        return mapping

    @staticmethod
    def combine(*mappings: "Mapping") -> "Mapping":
        """
        Combine multiple Mapping instances into one.

        :param mappings: Mapping instances to combine.
        :return: A new Mapping instance containing all mappings.
        """
        combined = Mapping()
        combined.__map = {}
        for mapping in mappings:
            for key in mapping.__map.keys():
                if key in combined.__map:
                    combined.__map[key] += mapping.__map[key]
                else:
                    combined.__map[key] = mapping.__map[key]
        return combined

    def get(
        self, key: str, default: Optional[str] = None, raise_error: bool = True
    ) -> str:
        """
        Get the value for a given key.

        :param key: The key to look up.
        :return: The corresponding value or None if not found.
        """
        if default is not None:
            raise_error = False
        if key in self.__map:
            assert (
                len(self.__map[key]) == 1
            ), "Multiple values found for key. Use get_with_context() instead."
            return self.__map[key][0]
        if raise_error:
            raise KeyError(f"Key '{key}' not found in mapping.")
        return default

    def get_with_context(self, key: str, context: str, fallback: str) -> str:
        """
        Retrieve the value associated with a given key, considering the provided context.
        This method uses a LanguageModel to estimate the probability of potential values given the context.
        The fallback value is included as one of the possible candidates.
        The value with the highest estimated probability is returned.
        If the key does not exist, the fallback value is returned.

        :param key: The key to look up.
        :param context: The context used to evaluate the likelihood of potential values.
        :param fallback: The fallback value.
        :return: The value with the highest estimated likelihood given the context.
        """
        lm = LanguageModelManager.get_language_model()
        if key in self.__map:
            values = self.__map[key] + (fallback,)
            max_score = float("-inf")
            best_value = fallback

            for value in values:
                score = lm.cond_score(value, context)
                if score > max_score:
                    max_score = score
                    best_value = value
            return best_value
        return fallback

    def contains(self, key: str) -> bool:
        """
        Check if the mapping contains a specific key.

        :param key: The key to check.
        :return: True if the key exists, False otherwise.
        """
        return key in self.__map
    
    def get_keys(self) -> Tuple[str]:
        return self.__map.keys()


class MappingManager:
    _registry = {}
    _lock = Lock()  # For thread-safety

    @classmethod
    def register_mapping(cls, name: str, mapping: Mapping):
        """
        Register a new mapping.

        :param name: The name of the mapping.
        :param mapping: An instance of Mapping to register.
        """
        with cls._lock:
            if name in cls._registry:
                logger.info(f"Mapping '{name}' is already registered.")
            cls._registry[name] = mapping

    @classmethod
    def get_mapping(cls, name: str) -> Mapping:
        """
        Retrieve a registered mapping by its name.

        :param name: The name of the mapping to retrieve.
        :return: The Mapping instance associated with the given name.
        :raises KeyError: If the mapping is not found.
        """
        with cls._lock:
            if name not in cls._registry:
                raise KeyError(f"Mapping '{name}' not found.")
            return cls._registry[name]
