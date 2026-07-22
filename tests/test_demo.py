"""Offline demo mode and API error handling (no network)."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import requests

from claimaudit.classifier import ClaimClassifier
from claimaudit.scholar import ScholarClient, ScholarError


class TestDemoMode:
    def test_search_returns_sample_papers(self):
        papers = ScholarClient(demo=True).search_topic("anything")
        assert len(papers) >= 3
        assert all(p.abstract for p in papers)

    def test_citations_available_for_demo_papers(self):
        client = ScholarClient(demo=True)
        papers = client.search_topic("anything")
        assert any(client.fetch_citations(p.paper_id) for p in papers)

    def test_audit_pipeline_runs_offline(self):
        results = ClaimClassifier(demo=True).audit_topic("anything")
        assert len(results) >= 1
        verdicts = {r.survival.verdict for r in results}
        # the bundled data is designed to produce more than one verdict
        assert len(verdicts) >= 2


class TestErrorHandling:
    def test_rate_limit_raises_scholar_error(self, monkeypatch):
        """Persistent 429s raise ScholarError, not a bare RuntimeError or empty result."""
        class _Resp:
            status_code = 429
            headers = {"Retry-After": "0"}

            def raise_for_status(self):  # pragma: no cover - not reached on 429
                pass

        client = ScholarClient()
        monkeypatch.setattr(client._session, "get", lambda *a, **k: _Resp())
        monkeypatch.setattr("claimaudit.scholar.time.sleep", lambda *_: None)
        with pytest.raises(ScholarError):
            client._get("paper/search", {})

    def test_network_failure_raises_scholar_error(self, monkeypatch):
        def _boom(*a, **k):
            raise requests.ConnectionError("no network")

        client = ScholarClient()
        monkeypatch.setattr(client._session, "get", _boom)
        monkeypatch.setattr("claimaudit.scholar.time.sleep", lambda *_: None)
        with pytest.raises(ScholarError):
            client._get("paper/search", {})
