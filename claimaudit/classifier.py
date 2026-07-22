"""Full pipeline: fetch papers -> extract claims -> match citations -> score."""

from __future__ import annotations

from dataclasses import dataclass, field

from claimaudit.scholar import ScholarClient, Paper
from claimaudit.extractor import ClaimExtractor, ClaimSentence
from claimaudit.matcher import match_citations, aggregate_labels
from claimaudit.scorer import compute_survival, ClaimSurvival


@dataclass
class AuditResult:
    paper: Paper
    claim: ClaimSentence
    survival: ClaimSurvival
    n_citations_fetched: int


class ClaimClassifier:
    def __init__(self, api_key: str = "", min_confidence: float = 0.5,
                 min_citations: int = 5, max_citations: int = 50,
                 demo: bool = False):
        self.client          = ScholarClient(api_key=api_key, demo=demo)
        self.extractor       = ClaimExtractor()
        self.min_confidence  = min_confidence
        self.min_citations   = min_citations
        self.max_citations   = max_citations

    def audit_topic(self, topic: str, n_papers: int = 10,
                    from_year: int = 2000, to_year: int = 2025) -> list[AuditResult]:
        """Full audit pipeline for a research topic."""
        papers  = self.client.search_topic(topic, limit=n_papers,
                                            from_year=from_year, to_year=to_year)
        results = []
        for paper in papers:
            if not paper.abstract:
                continue
            claims = self.extractor.extract(paper.abstract, self.min_confidence)
            if not claims:
                continue
            # use the highest-confidence claim per paper
            claim = max(claims, key=lambda c: c.confidence)
            try:
                citations = self.client.fetch_citations(paper.paper_id,
                                                         limit=self.max_citations)
            except Exception:
                citations = []

            matches        = match_citations(citations)
            label_counts   = aggregate_labels(matches)
            survival       = compute_survival(claim.text, label_counts,
                                              self.min_citations)
            results.append(AuditResult(
                paper=paper,
                claim=claim,
                survival=survival,
                n_citations_fetched=len(citations),
            ))
        return results
