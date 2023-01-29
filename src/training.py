"""
This module contains code for training models.
"""

from typing import List


class Vocabulary:
    """
    This class helps with assigning unique IDs to words, and encoding/decoding
    between the two representations.
    """

    UNKNOWN_INDEX = 0
    UNKNOWN_WORD = "<UNK>"

    def __init__(self, words: List[str]):
        unique = set(words)
        self.word_to_index = {word: i+1 for i, word in enumerate(unique)}
        self.index_to_word = {i+1: word for i, word in enumerate(unique)}

    def __len__(self):
        return len(self.word_to_index) + 1

    def get_index(self, word: str) -> int:
        """Get the index which corresponds to a word."""
        return self.word_to_index.get(word, Vocabulary.UNKNOWN_INDEX)

    def get_word(self, index: str) -> str:
        """Get the word which corresponds to an index."""
        return self.index_to_word.get(index, Vocabulary.UNKNOWN_WORD)

    def encode(self, words: List[str]) -> List[int]:
        """Encode a sequence of words into indices."""
        return [self.get_index(word) for word in words]

    def decode(self, indices: List[int]) -> List[str]:
        """Decode a sequence of indices back into words."""
        return [self.get_word(index) for index in indices]
