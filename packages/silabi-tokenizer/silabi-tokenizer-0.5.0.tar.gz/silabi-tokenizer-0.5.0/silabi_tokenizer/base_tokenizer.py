from abc import ABC, abstractmethod
from typing import List

class BaseTokenizer(ABC):


    def __call__(self, text: str):
        return self.tokenize(text)

    def tokenize(self, text: str) -> List[str]:
        raise NotImplementedError

    def tokens_to_ids(self, tokens: List[str]) -> List[int]:
        raise NotImplementedError

    def ids_to_tokens(self, ids : List[int]) -> List[str]:
        raise NotImplementedError

    def vocab_size(self) -> int:
        raise NotImplementedError
