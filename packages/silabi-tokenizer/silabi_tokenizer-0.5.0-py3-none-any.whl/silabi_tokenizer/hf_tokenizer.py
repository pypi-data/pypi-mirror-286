from typing import List
from transformers import PreTrainedTokenizer
from .kiswahili_tokenizer import KiswahiliTokenizer
import os
import json


class SilabiTokenizer(PreTrainedTokenizer):
    def __init__(self, *args, **kwargs):
        self.tokenizer = KiswahiliTokenizer()
        self.vocab = self.tokenizer.vocab
        self.ids_to_tokens = self.tokenizer.reverse_vocab
        super().__init__(*args, **kwargs)

    def _tokenize(self, text):
        return self.tokenizer.tokenize(text)

    def _convert_token_to_id(self, token):
        return self.tokenizer.tokens_to_ids([token])[0]

    def _convert_id_to_token(self, index):
        return self.tokenizer.convert_byte_token(self.ids_to_tokens.get(index, "<unk>"))

    def get_vocab(self):
        return self.vocab

    def vocab_size(self):
        return self.tokenizer.vocab_size()

    def save_vocabulary(self, save_directory=""):
        path = os.path.join(save_directory, "vocab.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.vocab, f, ensure_ascii=False, indent=4)
        return (path,)

    def build_inputs_with_special_tokens(
        self, token_ids_0: List[int], token_ids_1: List[int] | None = None
    ) -> List[int]:

        return [self.vocab["<s>"]] + token_ids_0 + [self.vocab["<s/>"]]

    def get_special_tokens_mask(
        self, token_ids_0, token_ids_1=None, already_has_special_tokens=False
    ):
        return [1] + ([0] * len(token_ids_0)) + [1]

    def create_token_type_ids_from_sequences(self, token_ids_0, token_ids_1=None):
        return len(token_ids_0) * [0] + ([1] * len(token_ids_1) if token_ids_1 else [])
