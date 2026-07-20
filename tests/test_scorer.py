"""Tests for ClaimAudit scorer."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from claimaudit.scorer import compute_survival, ClaimSurvival


CLAIM = "We show that the proposed method outperforms baseline approaches."


class TestComputeSurvival:
    def test_insufficient_data(self):
        s = compute_survival(CLAIM, {"confirms": 2, "challenges": 0}, min_citations=5)
        assert s.verdict == "insufficient data"
        assert s.score == 5.0

    def test_all_confirms_is_confirmed(self):
        s = compute_survival(CLAIM, {"confirms": 10, "challenges": 0, "extends": 0, "neutral": 0})
        assert s.verdict in ("confirmed", "well-supported")
        assert s.score >= 8.0

    def test_all_challenges_is_challenged(self):
        s = compute_survival(CLAIM, {"confirms": 0, "challenges": 10, "extends": 0, "neutral": 0})
        assert s.verdict == "challenged"
        assert s.score <= 2.0

    def test_mixed_gives_middle_score(self):
        s = compute_survival(CLAIM, {"confirms": 5, "challenges": 5, "extends": 0, "neutral": 0})
        assert 3.0 <= s.score <= 7.0

    def test_extends_adds_small_positive(self):
        s_base = compute_survival(CLAIM, {"confirms": 5, "challenges": 2, "extends": 0, "neutral": 3})
        s_ext  = compute_survival(CLAIM, {"confirms": 5, "challenges": 2, "extends": 5, "neutral": 3})
        assert s_ext.score >= s_base.score

    def test_score_in_range(self):
        for c, ch in [(0,10), (10,0), (5,5), (20,1)]:
            s = compute_survival(CLAIM, {"confirms": c, "challenges": ch})
            assert 0.0 <= s.score <= 10.0

    def test_claim_text_preserved(self):
        s = compute_survival(CLAIM, {"confirms": 8, "challenges": 1})
        assert s.claim_text == CLAIM

    def test_total_counts(self):
        s = compute_survival(CLAIM, {"confirms": 3, "challenges": 2, "extends": 1, "neutral": 2})
        assert s.total == 8

    def test_verdict_is_string(self):
        s = compute_survival(CLAIM, {"confirms": 6, "challenges": 2})
        assert isinstance(s.verdict, str) and len(s.verdict) > 0
