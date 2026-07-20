"""Match extracted claims to citation contexts and classify the relationship."""

from __future__ import annotations

import re
from dataclasses import dataclass

from claimaudit.scholar import CitationContext


_CONFIRM_PATTERNS = re.compile(
    r'\b(confirm|support|consistent with|agree|validate|replicate|extend|'
    r'in line with|corroborate|consistent|verify)\b',
    re.I
)
_CHALLENGE_PATTERNS = re.compile(
    r'\b(contradict|challenge|dispute|refute|contrary|inconsistent|fail to replicate|'
    r'not (support|consistent|replicate)|question|undermine|conflict)\b',
    re.I
)
_EXTEND_PATTERNS = re.compile(
    r'\b(build on|extend|generalize|apply to|expand|further|beyond|improve upon)\b',
    re.I
)


@dataclass
class MatchResult:
    citation: CitationContext
    relation: str    # "confirms" | "challenges" | "extends" | "neutral"
    confidence: float


def classify_citation(ctx: CitationContext) -> MatchResult:
    """
    Classify how a citing paper relates to the source claim.
    Uses intents first (from Semantic Scholar), falls back to context text.
    """
    intents = [i.lower() for i in ctx.intents]

    # semantic scholar provides structured intents when available
    if "result" in intents or "methodology" in intents:
        # "result" intents usually mean the work built on / confirmed
        if ctx.is_influential:
            return MatchResult(ctx, "confirms", 0.8)
        return MatchResult(ctx, "extends", 0.65)

    text = ctx.context_text
    if not text:
        return MatchResult(ctx, "neutral", 0.5)

    challenge_m = _CHALLENGE_PATTERNS.search(text)
    confirm_m   = _CONFIRM_PATTERNS.search(text)
    extend_m    = _EXTEND_PATTERNS.search(text)

    if challenge_m and not confirm_m:
        return MatchResult(ctx, "challenges", 0.75)
    if confirm_m and not challenge_m:
        return MatchResult(ctx, "confirms", 0.75)
    if extend_m:
        return MatchResult(ctx, "extends", 0.65)
    return MatchResult(ctx, "neutral", 0.5)


def match_citations(citations: list[CitationContext]) -> list[MatchResult]:
    """Classify all citations for a paper."""
    return [classify_citation(c) for c in citations]


def aggregate_labels(results: list[MatchResult]) -> dict[str, int]:
    """Count each relation label across all citation matches."""
    counts: dict[str, int] = {"confirms": 0, "challenges": 0, "extends": 0, "neutral": 0}
    for r in results:
        counts[r.relation] = counts.get(r.relation, 0) + 1
    return counts
