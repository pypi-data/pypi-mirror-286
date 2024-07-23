from .base_tokenizer import BaseTokenizer
from .silabi_generator import SilabiVocabGenerator
import os
import re
import logging
import json
from typing import List

logger = logging.getLogger(__name__)


class KiswahiliTokenizer(BaseTokenizer):
    """
    Preferred
    Kiswahili Syllabic Tokenizer. With a byte fallback to utf-8.
    Generates a vocabulary file if not found.
    """

    def __init__(self) -> None:
        if not os.path.exists("silabi_vocab.json"):
            logger.debug("silabi_vocab.json not found, generating one")
            vocab = SilabiVocabGenerator()
            lookup = vocab.generate_silabi_lookup()
            vocab.write_to_file("silabi_vocab.json")
            self.vocab = lookup
        else:
            with open("silabi_vocab.json", "r") as f:
                self.vocab = json.load(f)
        self.reverse_vocab = {v: k for k, v in self.vocab.items()} # used for reverse lookup. from id to token
    
    def __call__(self, text: str):
        
        return self.tokenize(text)

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenizes the text on the syllables
        """
        # add an initial whitespace to the text
        text = f" {text}"
        # replace the whitespace with _
        text = text.replace(" ", "_")
        syllables = []
        while len(text) > 0:
            found = False
            for i in range(1, 6):
                if text[:i] in self.vocab:
                    syllables.append(text[:i])
                    text = text[i:]
                    found = True
                    break
            if not found:
                syllables.append(text[0])
                text = text[1:]
        return syllables

    def tokens_to_ids(self, tokens: list) -> List[int]:
        """
        Converts tokens to their ids
        """
        ids = []
        for token in tokens:
            try:
                if token in self.vocab:
                    ids.append(self.vocab[token])
                else:
                    # utf byte fallback
                    ids.append(self.vocab[f"<0x{ord(token):02x}>"])
            except KeyError as _:
                ids.append(self.vocab["<unk>"])

        return ids

    def convert_byte_token(self, token: str) -> str:
        """
        Converts a byte token to its utf-8 representation
        """
        pattern = r"<0x([0-9A-Fa-f]{1,2})>"
        match = re.match(pattern, token)
        if match:
            return chr(int(match.group(1), 16))
        return token

    def ids_to_tokens(self, ids: List[int]) -> List[str]:
        """
        Converts ids to their tokens
        """

        return [self.convert_byte_token(self.reverse_vocab[id]) for id in ids]

    def vocab_size(self) -> int:
        """
        Returns the size of the vocabulary
        """
        return list(self.vocab.values())[-1] +1

    def tokens_to_sentence(self, tokens: List[str]) -> str:
        """
        Converts tokens to a sentence.
        Removes special tokens from the result sentence.
        """
        return "".join(tokens).replace("_", " ").replace('<unk>','').strip()

    def __repr__(self) -> str:
        return f"SilabiTokenizer()"

    @property
    def pad_token(self):
        return self.vocab["<pad>"]

    @property
    def bos_token(self):
        return self.vocab["<s>"]

    @property
    def eos_token(self):
        return self.vocab["<s/>"]

    @property
    def unk_token(self):
        return self.vocab["<unk>"]



if __name__ == "__main__":
    # Initialize the tokenizer
    tokenizer = KiswahiliTokenizer()
    # Encode a sample text
    encoded_input = tokenizer("Mfano Kenya.")
    print(encoded_input)