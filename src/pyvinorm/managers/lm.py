import logging

from typing import List
from threading import Lock

import kenlm

logger = logging.getLogger(__name__)


class LanguageModel:
    r"""A simple N-gram language model.

    This class estimate the conditional log probability of a text given a context
    :math:`logP(text|context)` using a pre-trained KenLM model.

    The text :math:`T` and context :math:`C` can contains multiple words:
    :math:`T = s_ks_{k+1}...s_{m}` and :math:`C = s_1s_2...s_{k-1}`.
    The conditional score :math:`logP(T|C)` is approximated using N-order Markov assumption:
    .. math::
        logP(T|C) \approx logP(s_ks_{k+1}...s_{k+n} | s_{k-n+1}s_{k-n+2}...s_{k-1}) \
                  \approx \frac{1}{n-1} \sum_{i=k}^{k+n-2} logP(s_t | s_{t-2}s_{t-1})
    where n is the order of the N-gram model.
    """

    @staticmethod
    def from_file(model_path: str):
        model = LanguageModel()
        model.model = kenlm.LanguageModel(model_path)
        model.n_order = model.model.order
        return model

    def cond_score(self, text: str, context: str):
        """
        Computes the conditional score :math:`logP(text|context)`
        of a text given a context.

        **Notes:**
        - Only n - 1 last words of context is taken to calculating the score.
        - Only n - 1 first words of text is taken to calculating the score.
        - Words in text and context are extracted by simply call `.split()`. Therefore,
        they should be tokenized beforehand.

        :param str text: The text to score.
        :param str context: The context in which the text is evaluated.
        :return float: The conditional score of the text given the context.
        """
        text = text.split()
        context = context.split()

        score = 0
        for i in range(min(len(text), self.n_order - 1)):
            w = text[i]
            c = context[-(self.n_order - i - 1) :]
            if i > 0:
                c += text[:i]

            c = " ".join(c)
            score += self.model.score(
                c + " " + w, bos=False, eos=False
            ) - self.model.score(c, bos=False, eos=False)
        score = score / (i + 1)
        return score


class LanguageModelManager:
    _language_model = None
    _lock = Lock()  # For thread-safety

    @classmethod
    def register_language_model(cls, language_model: LanguageModel):
        with cls._lock:
            if cls._language_model is not None:
                logger.info(f"Language model is already registered.")
            cls._language_model = language_model

    @classmethod
    def get_language_model(cls) -> LanguageModel:
        with cls._lock:
            if cls._language_model is None:
                raise KeyError(f"Language model not found.")
            return cls._language_model
