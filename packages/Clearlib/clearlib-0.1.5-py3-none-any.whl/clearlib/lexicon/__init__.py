"""Utilities for working with source language lexicons.

Resources include:
- [UBS Dictionary of the Greek New
  Testament](https://github.com/ubsicap/ubs-open-license/tree/main/dictionaries/greek)
- [UBS Dictionary of Biblical
  Hebrew](https://github.com/ubsicap/ubs-open-license/tree/main/dictionaries/hebrew)

"""

from .LexiconEntry import LEXSense, LEXMeaning, BaseForm, Lexicon_Entry
from .ubsdgnt import UBSParser, get_ubsdgnt

__all__ = [
    # LexiconEntry
    "LEXSense",
    "LEXMeaning",
    "BaseForm",
    "Lexicon_Entry",
    # ubsdgnt
    "UBSParser",
    "get_ubsdgnt",
]
