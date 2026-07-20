"""Semantic Scholar API client for fetching papers and their citations."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import requests

BASE_URL   = "https://api.semanticscholar.org/graph/v1"
RATE_SLEEP = 1.5   # seconds between requests (free tier limit)
MAX_RETRY  = 3


@dataclass
class Author:
    name: str
    author_id: str = ""


@dataclass
class Paper:
    paper_id: str
    title: str
    abstract: str
    year: int | None
    authors: list[Author] = field(default_factory=list)
    citation_count: int = 0


@dataclass
class CitationContext:
    paper_id: str
    title: str
    year: int | None
    intents: list[str]       # "methodology", "background", "result"
    is_influential: bool
    context_text: str = ""


class ScholarClient:
    def __init__(self, api_key: str = ""):
        self._session = requests.Session()
        if api_key:
            self._session.headers["x-api-key"] = api_key

    def _get(self, path: str, params: dict) -> dict:
        url = f"{BASE_URL}/{path}"
        for attempt in range(MAX_RETRY):
            resp = self._session.get(url, params=params, timeout=10)
            if resp.status_code == 429:
                time.sleep(RATE_SLEEP * (attempt + 2))
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError(f"Max retries exceeded for {path}")

    def search_topic(self, query: str, limit: int = 20,
                     from_year: int = 2000, to_year: int = 2025) -> list[Paper]:
        """Search for papers on a topic with year filters."""
        data   = self._get("paper/search", {
            "query":  query,
            "limit":  limit,
            "fields": "paperId,title,abstract,year,authors,citationCount",
            "year":   f"{from_year}-{to_year}",
        })
        papers = []
        for item in data.get("data", []):
            authors = [Author(a.get("name",""), a.get("authorId",""))
                       for a in item.get("authors", [])]
            papers.append(Paper(
                paper_id=item.get("paperId",""),
                title=item.get("title",""),
                abstract=item.get("abstract","") or "",
                year=item.get("year"),
                authors=authors,
                citation_count=item.get("citationCount", 0),
            ))
            time.sleep(RATE_SLEEP)
        return papers

    def fetch_citations(self, paper_id: str, limit: int = 50) -> list[CitationContext]:
        """Fetch citing papers and their citation context/intent."""
        data  = self._get(f"paper/{paper_id}/citations", {
            "limit":  limit,
            "fields": "paperId,title,year,intents,isInfluential,contexts",
        })
        ctxs  = []
        for item in data.get("data", []):
            citing = item.get("citingPaper", {})
            ctxs.append(CitationContext(
                paper_id=citing.get("paperId",""),
                title=citing.get("title",""),
                year=citing.get("year"),
                intents=item.get("intents", []),
                is_influential=item.get("isInfluential", False),
                context_text=" ".join(item.get("contexts", [])),
            ))
        time.sleep(RATE_SLEEP)
        return ctxs
