"""Tests for ClaimExtractor and matcher helpers (no network required)."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from claimaudit.extractor import ClaimExtractor, ClaimSentence
from claimaudit.matcher import classify_citation, aggregate_labels
from claimaudit.scholar import CitationContext


@pytest.fixture
def extractor():
    return ClaimExtractor()


class TestClaimExtractor:
    def test_extracts_we_show(self, extractor):
        abstract = "We show that federated learning reduces data leakage significantly."
        claims = extractor.extract(abstract)
        assert len(claims) >= 1

    def test_no_claim_in_plain_text(self, extractor):
        abstract = "The sky is blue. Water is wet. Trees grow tall."
        claims = extractor.extract(abstract)
        assert len(claims) == 0

    def test_has_claim_returns_true(self, extractor):
        abstract = "We demonstrate that the approach converges in O(n log n)."
        assert extractor.has_claim(abstract) is True

    def test_has_claim_returns_false(self, extractor):
        abstract = "The dataset contains 10,000 samples collected over six months."
        assert extractor.has_claim(abstract) is False

    def test_confidence_in_range(self, extractor):
        abstract = "This paper introduces a novel method for text classification."
        for claim in extractor.extract(abstract):
            assert 0.0 <= claim.confidence <= 1.0

    def test_signal_field_nonempty(self, extractor):
        abstract = "We find that regularisation reduces overfitting."
        claims = extractor.extract(abstract)
        for c in claims:
            assert len(c.signal) > 0

    def test_min_confidence_filter(self, extractor):
        abstract = "Our study finds a weak correlation. We show evidence."
        all_c    = extractor.extract(abstract, min_confidence=0.0)
        high_c   = extractor.extract(abstract, min_confidence=0.9)
        assert len(high_c) <= len(all_c)


class TestClassifyCitation:
    def _make_ctx(self, intents, is_influential=False, context_text=""):
        return CitationContext(
            paper_id="123", title="Test", year=2022,
            intents=intents, is_influential=is_influential,
            context_text=context_text,
        )

    def test_influential_result_is_confirms(self):
        ctx = self._make_ctx(["result"], is_influential=True)
        r   = classify_citation(ctx)
        assert r.relation == "confirms"

    def test_challenge_text_is_challenges(self):
        ctx = self._make_ctx([], context_text="This contradicts the previous finding.")
        r   = classify_citation(ctx)
        assert r.relation == "challenges"

    def test_support_text_is_confirms(self):
        ctx = self._make_ctx([], context_text="Consistent with their work, we also find X.")
        r   = classify_citation(ctx)
        assert r.relation == "confirms"

    def test_empty_context_is_neutral(self):
        ctx = self._make_ctx([], context_text="")
        r   = classify_citation(ctx)
        assert r.relation == "neutral"

    def test_aggregate_counts(self):
        from claimaudit.matcher import MatchResult
        results = [
            MatchResult(self._make_ctx([]), "confirms",   0.8),
            MatchResult(self._make_ctx([]), "confirms",   0.8),
            MatchResult(self._make_ctx([]), "challenges", 0.7),
            MatchResult(self._make_ctx([]), "neutral",    0.5),
        ]
        counts = aggregate_labels(results)
        assert counts["confirms"]   == 2
        assert counts["challenges"] == 1
        assert counts["neutral"]    == 1
