"""Read the UBS dictionaries into lookup dicts.

The dataclass reflect the XML hierarchy (selectively):
Lexicon_Entry.baseforms ->
BaseForm.lexMeanings ->
LEXMeaning.lexSenses ->
LEXSense
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class LEXSense:
    """Represents the same element from UBSGNT as a Python dataclass."""

    # no distinct identifier: 1-1 with LEXMeaning for Greek
    # the language of the definition
    languageCode: str
    glosses: list[str]
    definitionShort: str
    definitionLong: str
    comments: list[str]
    # link upward: beware recursion
    parent: Optional["LEXMeaning"] = field(init=False, default=None)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"<LEXSense: {';'.join(self.glosses)}>"

    def asdict(self) -> dict[str, Any]:
        """Return content as dict, minus the parent to avoid infinite recursion."""
        fields = ["languageCode", "glosses", "definitionShort", "definitionLong", "comments"]
        return {f: getattr(self, f) for f in fields}


@dataclass
class LEXMeaning:
    """Represents the same element from UBSGNT as a Python dataclass."""

    identifier: str
    isBiblicalTerm: str
    entryCode: str
    lexDomains: list[str]
    lexSubDomains: list[str]
    # appears to only be one LEXSense per LEXMeaning? But the
    # structure allows for more
    lexSenses: list[LEXSense]
    # using MARBLE-style references
    # this includes the deuterocanon, which seems to often have
    # multiple meanings for a single reference
    # some unusual ones like '04500900300002{N:002}'
    lexReferences: list[str]
    # link upward: beware recursion
    parent: Optional["BaseForm"] = field(init=False, default=None)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"<LEXMeaning: {self.identifier}>"

    def __hash__(self) -> int:
        """Return a hash value."""
        return hash(self.identifier)

    def asdict(self) -> dict[str, Any]:
        """Return content as dict, minus the parent to avoid infinite recursion."""
        fields = ["identifier", "isBiblicalTerm", "entryCode", "lexDomains", "lexSubDomains"]
        return {f: getattr(self, f) for f in fields}


@dataclass
class BaseForm:
    """Represents the same element from UBSGNT as a Python dataclass."""

    identifier: str
    partsofspeech: list[str]
    lexMeanings: list[LEXMeaning]
    # FUTURE: incorporate RelatedLemmas.L
    # link upward: beware recursion
    parent: Optional["Lexicon_Entry"] = field(init=False, default=None)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"<BaseForm: {self.identifier}>"

    def __hash__(self) -> int:
        """Return a hash value."""
        return hash(self.identifier)

    def asdict(self) -> dict[str, Any]:
        """Return content as dict, minus the parent to avoid infinite recursion."""
        fields = ["identifier", "partsofspeech"]
        return {f: getattr(self, f) for f in fields}


@dataclass
class Lexicon_Entry:
    """Represents the same element from UBSGNT as a Python dataclass."""

    identifier: str
    lemma: str
    strongCodes: list[str]
    # FUTURE: capture Notes (see Lexicon_Entry Id="003076000000000")
    # multiple values if different parts of speech,
    # e.g. <Lexicon_Entry: 000266000000000>
    baseforms: list[BaseForm]

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"<Lexicon_Entry: {self.identifier}>"

    def __hash__(self) -> int:
        """Return a hash value."""
        return hash(self.identifier)

    def get_meanings(self) -> list[LEXMeaning]:
        """Return a list of of LEXMeanings for this entry."""
        return [lm for bf in self.baseforms for lm in bf.lexMeanings]
