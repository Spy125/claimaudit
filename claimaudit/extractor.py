"""Extract claim sentences from paper abstracts using signal words."""

from __future__ import annotations

import re
from dataclasses import dataclass

_CLAIM_SIGNALS = re.compile(
    r'\b(we (show|demonstrate|find|argue|propose|present|introduce|claim)|'
    r'(this|our) (paper|work|study|approach|method) (shows?|demonstrates?|'
    r'introduces?|presents?|proposes?|finds?)|results? (show|suggest|indicate)|'
    r'(it is|we) (shown?|demonstrated?|found?) that|'
    r'we (conclude|establish|prove) that|'
    r'(our|the) (main|primary|key) (claim|contribution|finding|result))\b',
    re.I
)

_ABBREV = re.compile(r'\b(Dr|Mr|Mrs|Prof|Fig|et al|e\.g|i\.e|vs)\.')


@dataclass
class ClaimSentence:
    text: str
    signal: str        # the matched signal word/phrase
    confidence: float  # 0-1


def _split_sentences(text: str) -> list[str]:
    """Split on periods while protecting known abbreviations."""
    protected = _ABBREV.sub(lambda m: m.group().replace(".", "\x00"), text)
    raw       = re.split(r'(?<=[.!?])\s+', protected)
    return [s.replace("\x00", ".").strip() for s in raw if s.strip()]


class ClaimExtractor:
    def extract(self, abstract: str, min_confidence: float = 0.5) -> list[ClaimSentence]:
        """Find claim sentences in a paper abstract."""
        sentences = _split_sentences(abstract)
        claims    = []
        for sent in sentences:
            m = _CLAIM_SIGNALS.search(sent)
            if m:
                # longer matches get slightly higher confidence
                conf = min(0.95, 0.6 + len(m.group()) * 0.01)
                if conf >= min_confidence:
                    claims.append(ClaimSentence(
                        text=sent,
                        signal=m.group(),
                        confidence=round(conf, 2),
                    ))
        return claims

    def has_claim(self, abstract: str) -> bool:
        return bool(_CLAIM_SIGNALS.search(abstract))
