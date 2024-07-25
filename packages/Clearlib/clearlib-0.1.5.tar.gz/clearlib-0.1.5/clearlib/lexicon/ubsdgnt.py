"""Parse UBSGNT into dataclasses.

>>> from clearlib.lexicon import UBSParser
>>> ubsprs = UBSParser()
>>> len(ubsprs)
5507
# check whether a lemma is included
>>> "ἀκούω" in ubsprs.lemma_entries
True
# look up an lexicon entry by lemma
>>> akouo = ubsprs.get_lemma_entries("ἀκούω")
>>> akouo
<Lexicon_Entry: 000188000000000>
# look at the meanings and senses for a lexicon entry
# for DGNT, looks like only one sense per meaning
>>> akouo.get_meanings()
akouo.get_meanings()
[<LEXMeaning: 000188001001000>, <LEXMeaning: 000188001002000>, ...]
# 10 meanings: are they all biblical? Yes.
>>> len(akouo.get_meanings())
10
>>> len([lexmean for lexmean in akouo.get_meanings() if lexmean.isBiblicalTerm])
10
>>> for lexmeaning in akouo.get_meanings():
...   print(lexmeaning.lexSenses[0])
<LEXSense: to hear;hearing{N:001}>
<LEXSense: to be able to hear;faculty of hearing>
<LEXSense: to receive news;to hear>
<LEXSense: to accept;to listen to;to listen and respond;to pay attention and respond;to heed>
<LEXSense: to pay attention to and obey>
<LEXSense: to understand;to comprehend>
<LEXSense: to hear a case;to provide a legal hearing;to hear a case in court>
<LEXSense: to hear in secret>
<LEXSense: to be slow to understand;to be mentally dull>
<LEXSense: to listen carefully;to listen and listen>
# get more detailed information about a particular sense
>>> akouo3 = akouo.get_meanings()[3].lexSenses[0]
>>> akouo3
<LEXSense: to accept;to listen to;to listen and respond;to pay attention and respond;to heed>
>>> import pprint
>>> pprint.pprint(akouo3.asdict())
{'comments': [],
 'definitionLong': '',
 'definitionShort': 'to believe something and to respond to it on the basis of '
                    'having heard',
 'glosses': ['to accept',
             'to listen to',
             'to listen and respond',
             'to pay attention and respond',
             'to heed'],
 'languageCode': 'en'}
# you can retrieve the parent of a sense: it has different fields
>>> pprint.pprint(akouo3.parent.asdict())
{'entryCode': '31.56',
 'identifier': '000188001004000',
 'isBiblicalTerm': 'Y',
 'lexDomains': ['Hold a View, Believe, Trust'],
 'lexSubDomains': ['Accept As True']}

"""

from collections import UserDict, defaultdict
from typing import Any
import unicodedata

import requests
from lxml import etree

from biblelib.word import bcvwpid

from .LexiconEntry import LEXSense, LEXMeaning, BaseForm, Lexicon_Entry


def get_ubsdgnt(langcode: str = "eng") -> str:
    """Return a string for the readable content from Github."""
    pathprefix: str = (
        "https://github.com/ubsicap/ubs-open-license/raw/main/dictionaries/greek/XML/UBSGreekNTDic-v1.0"
    )
    langcodes = {
        "eng": "en",
        "fra": "fr",
        "spa": "sp",
        # not ISO 639-3
        "zhs": "zhs",
        "zht": "zht",
    }
    return f"{pathprefix}-{langcodes[langcode]}.XML"


class UBSParser(UserDict):
    """Manage data read from UBSGNT."""

    # for lookup methods
    lemma_entries: dict[str, Lexicon_Entry] = {}
    entryCode_meanings: dict[str, LEXMeaning] = {}
    # sometimes multiple meanings for a word-level reference
    reference_meanings: dict[str, list[LEXMeaning]] = defaultdict(list)

    def __init__(self, langcode: str = "eng"):
        """Initialize the parser."""
        super().__init__()
        # these store elements for debugging
        # unfollowed import problem, so values are Any
        self.lexicon_entries: dict[str, Any] = {}
        self.baseform_elements: dict[str, Any] = {}
        self.lexmeaning_elements: dict[str, Any] = {}
        self.dicturi = get_ubsdgnt(langcode)
        r = requests.get(self.dicturi)
        assert r.status_code == 200, f"Failed to get content from {self.dicturi}"
        # normalize everything so matching works
        self.root = etree.fromstring(r.text)
        # iterate over Lexicon_Entry elements
        # for Greek, each Lexicon_Entry.lemma is unique, so could use
        # lemma for keys rather than identifier. Not sure about Hebrew though
        self.data = {
            thislexe.identifier: thislexe
            for lexentry in self.root.xpath("//Lexicon_Entry")
            if (thislexe := self.do_lexicon_entry(lexentry))
        }

    @staticmethod
    def _first_if(xpathexpr: str) -> str:
        """Return first string value in the xpath result, or empty string."""
        return xpathexpr[0] if len(xpathexpr) > 0 else ""

    # type complaint with this
    #    def do_senses(self, lexmean: etree._Element) -> list[LEXSense]:
    def do_senses(self, lexmean: Any) -> list[LEXSense]:
        """Process LEXSense content.

        Returns a list with a single LEXSense instance. This leaves
        room for other data that might have multiple.

        """
        # only ever one LEXSense for Greek
        lexsense = lexmean.xpath("LEXSenses/LEXSense")[0]
        lsdict = dict(
            languageCode=lexsense.xpath("@LanguageCode")[0],
            glosses=lexsense.xpath("Glosses/Gloss/text()"),
            definitionShort=self._first_if(lexsense.xpath("DefinitionShort/text()")),
            definitionLong=self._first_if(lexsense.xpath("DefinitionLong/text()")),
            comments=lexsense.xpath("Comments/Comment/text()"),
        )
        return [LEXSense(**lsdict)]

    # def do_meaning(self, lexmean: etree._Element) -> LEXMeaning:
    def do_meaning(self, lexmean: Any) -> LEXMeaning:
        """Process LEXMeaning contents."""
        # stash for debugging
        lexmean_id: str = lexmean.xpath("@Id")[0]
        self.lexmeaning_elements[lexmean_id] = lexmean
        try:
            lexsenses = self.do_senses(lexmean)
        except Exception as e:
            print(f"Failed on {lexmean}, {lexmean_id}\n{e}")
            lexsenses = []
        try:
            lexReferences = [
                bcvwpid.fromubs(ref).get_id()
                for ref in lexmean.xpath("LEXReferences/LEXReference/text()")
            ]
        except Exception as e:
            print(f"Failed on references for {lexmean}, {lexmean_id}\n{e}")
            lexReferences = []
        lexmeaning = LEXMeaning(
            identifier=lexmean_id,
            isBiblicalTerm=self._first_if(lexmean.xpath("@IsBiblicalTerm")),
            entryCode=self._first_if(lexmean.xpath("@EntryCode")),
            # does this capture multiple values correctly?
            lexDomains=lexmean.xpath("LEXDomains/LEXDomain/text()"),
            lexSubDomains=lexmean.xpath("LEXSubDomains/LEXSubDomain/text()"),
            lexSenses=lexsenses,
            lexReferences=lexReferences,
        )
        for lexs in lexsenses:
            lexs.parent = lexmeaning
        return lexmeaning

    def do_baseform(self, baseformel: Any) -> BaseForm:
        """Process BaseForm contents."""
        # stash for debugging
        baseform_id: str = baseformel.xpath("@Id")[0]
        self.baseform_elements[baseform_id] = baseformel
        baseform = BaseForm(
            identifier=baseform_id,
            partsofspeech=baseformel.xpath("PartsOfSpeech/PartOfSpeech/text()"),
            lexMeanings=[
                self.do_meaning(lm)
                for lm in baseformel.xpath("LEXMeanings/LEXMeaning")
                if self._first_if(lm.xpath("@IsBiblicalTerm")) != "N"
            ],
        )
        for lm in baseform.lexMeanings:
            lm.parent = baseform
        return baseform

    def do_lexicon_entry(self, lexentry: Any) -> Lexicon_Entry:
        """Process Lexicon_Entry contents."""
        lexentry_id: str = lexentry.xpath("@Id")[0]
        self.lexicon_entries[lexentry_id] = lexentry
        # PROCESS do_baseform here
        thislexe = Lexicon_Entry(
            identifier=lexentry_id,
            lemma=unicodedata.normalize("NFKC", lexentry.xpath("@Lemma")[0]),
            strongCodes=lexentry.xpath("StrongCodes/Strong/text()"),
            # this assumes a single BaseForm per lexentry
            baseforms=[self.do_baseform(bf) for bf in lexentry.xpath("BaseForms/BaseForm")],
        )
        for bf in thislexe.baseforms:
            bf.parent = thislexe
        return thislexe

    # accessors
    # only build these on demand

    # just make lemma the key for self.data?
    def get_lemma_entries(self, lemma: str) -> Lexicon_Entry:
        """Return the Lexicon_Entry instance for lemma."""
        if not self.lemma_entries:
            self.lemma_entries = {entry.lemma: entry for entry in self.data.values()}
        return self.lemma_entries[lemma]

    def get_entryCode_meanings(self, entryCode: str) -> LEXMeaning:
        """Return the LEXMeaning instance for an entryCode."""
        if not self.entryCode_meanings:
            self.entryCode_meanings = {
                meaning.entryCode: meaning
                for entry in self.data.values()
                for baseform in entry.baseforms
                for meaning in baseform.lexMeanings
            }
        return self.entryCode_meanings[entryCode]

    def get_reference_meanings(self, reference: str) -> list[LEXMeaning]:
        """Return the LEXMeaning instances for an reference."""
        if not self.reference_meanings:
            for entry in self.data.values():
                for baseform in entry.baseforms:
                    for meaning in baseform.lexMeanings:
                        for ref in meaning.lexReferences:
                            self.reference_meanings[ref].append(meaning)
        return self.reference_meanings[reference]

    def get_strongs_lemmas(self) -> dict[str, list[Lexicon_Entry]]:
        """Return a mapping from strongs to lemmas."""
        strongs_lemmas: dict[str, list[Lexicon_Entry]] = defaultdict(list)
        for entry in self.data.values():
            for strong in entry.strongCodes:
                strongs_lemmas[strong].append(entry)
        return strongs_lemmas

    def get_strongs_meanings(self) -> dict[str, list[LEXMeaning]]:
        """Return a mapping from strongs to lexMeanings."""
        strongs_lemmas: dict[str, list[LEXMeaning]] = defaultdict(list)
        for entry in self.data.values():
            for baseform in entry.baseforms:
                for meaning in baseform.lexMeanings:
                    for strong in entry.strongCodes:
                        strongs_lemmas[strong].append(meaning)
        return strongs_lemmas
