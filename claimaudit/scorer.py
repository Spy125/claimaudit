"""Score each claim based on how many citations confirm vs challenge it.

Formula: (confirms*2 + extends*0.5 - challenges*2) / total, scaled to 0-10.

Verdicts:
  9-10 : Strongly confirmed
  7-8  : Well-supported
  5-6  : Mixed / inconclusive
  3-4  : Contested
  0-2  : Largely challenged
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ClaimSurvival:
    claim_text: str
    confirms: int
    challenges: int
    extends: int
    neutral: int
    total: int
    score: float      # 0-10
    verdict: str      # "confirmed" | "contested" | "challenged" | "insufficient data"


_WEIGHTS = {"confirms": 2.0, "extends": 0.5, "challenges": -2.0, "neutral": 0.0}
_VERDICT_THRESHOLDS = [
    (8.0, "confirmed"),
    (6.0, "well-supported"),
    (4.5, "mixed"),
    (3.0, "contested"),
    (0.0, "challenged"),
]


def compute_survival(
    claim_text: str,
    label_counts: dict[str, int],
    min_citations: int = 5,
) -> ClaimSurvival:
    """Compute survival score for one claim."""
    confirms   = label_counts.get("confirms", 0)
    challenges = label_counts.get("challenges", 0)
    extends    = label_counts.get("extends", 0)
    neutral    = label_counts.get("neutral", 0)
    total      = confirms + challenges + extends + neutral

    if total < min_citations:
        return ClaimSurvival(
            claim_text=claim_text,
            confirms=confirms, challenges=challenges,
            extends=extends, neutral=neutral, total=total,
            score=5.0,
            verdict="insufficient data",
        )

    raw          = sum(_WEIGHTS[k] * v for k, v in label_counts.items() if k in _WEIGHTS)
    max_possible = total * 2.0
    # shift so 0 confirms/challenges gives score of 5
    normalised   = (raw / max_possible + 0.5) * 10
    score        = max(0.0, min(10.0, normalised))

    verdict = "challenged"
    for threshold, label in _VERDICT_THRESHOLDS:
        if score >= threshold:
            verdict = label
            break

    return ClaimSurvival(
        claim_text=claim_text,
        confirms=confirms, challenges=challenges,
        extends=extends, neutral=neutral, total=total,
        score=round(score, 1),
        verdict=verdict,
    )
