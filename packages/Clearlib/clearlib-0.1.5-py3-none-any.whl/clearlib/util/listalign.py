"""Given two lists of terms, return the best alignment between them.

>>> from clearlib.util import listalign
>>> al = listalign.Aligner(terms1, terms2)
>>> al.write_tsv(somepath)

'Best' is determined by computing Levenstein edit distance between
each pair of terms, and selecting the pairing with the greatest
similarity.

Any duplicates in list2 are collapsed.
The best mapping for each item in the first list is computed
independently of others: so a term in the second list might be mapped
multiple times.

"""

from collections.abc import Callable
from pathlib import Path
from statistics import mean

from thefuzz import fuzz


def compare(term1: list[str], term2: list[str]) -> float:
    """Return a probability that the two term lists are similar.

    Lower-cases terms before comparison. If args are a list of terms,
    return the mean across pairings.

    """
    ratio: float = mean(fuzz.ratio(t1.lower(), t2.lower()) / 100 for t1 in term1 for t2 in term2)
    return ratio


class Aligner:
    """Align two lists of terms.

    This compares NxM (and each can be multiple terms), so it's
    expensive for larger datasets.

    """

    def __init__(
        self,
        terms1: list[str],
        terms2: list[str],
        cmp: Callable[[list[str], list[str]], float] = compare,
    ) -> None:
        """Initialize an instance."""
        self.terms1 = terms1
        self.terms2 = terms2
        # term from terms1 -> (term2 -> score)
        self.matrix: dict[str, dict[str, float]]
        # might be more efficient to do this spliting once and cache it
        self.matrix = {
            t1: {t2: cmp(t1.split(","), t2.split(",")) for t2 in terms2} for t1 in terms1
        }

    def matches(self, t1: str, threshold: float = 0.5) -> list[str]:
        """Return matches for t1 above threshold."""
        candidates = [pair for pair in self.matrix[t1].items() if pair[1] > threshold]
        mapped = sorted(candidates, key=lambda pair: pair[1], reverse=True)
        return [m[0] for m in mapped]

    def write_tsv(self, outpath: Path) -> None:
        """Output matches, and unmatched items from terms2."""
        matched: set[str] = set()
        with outpath.open("w") as f:
            for t1 in self.matrix:
                mapped = self.matches(t1)
                # tracks what's been mapped
                for m in mapped:
                    matched.add(m)
                mappedstr = "; ".join(mapped)
                f.write(f"{t1}\t{mappedstr}\n")
            # now output what wasn't mapped
            for t2 in self.terms2:
                if t2 not in matched:
                    f.write(f"\t{t2}\n")
