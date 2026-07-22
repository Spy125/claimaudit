# ClaimAudit

Tracks how well the empirical claims in a research paper hold up over time. Given a paper PDF or DOI, it extracts quantitative and causal claims from the abstract and body, finds citing papers via the Semantic Scholar API, and classifies each citation as confirming, challenging, or extending the original claim. The result is a per-claim survival report.

Built to explore NLP pipelines on academic text and to think about how scientific consensus forms (or doesn't) after publication.

---

## How it works

1. Claims are extracted from the paper using regex signals for quantitative, comparative, and causal language
2. Each claim is deduplicated using Jaccard similarity to remove near-duplicates
3. Citing papers are retrieved from Semantic Scholar (free, no API key required)
4. Citation contexts are matched to claims using TF-IDF cosine similarity
5. Each context is classified as: confirms / challenges / extends / neutral
6. A survival score is computed per claim: `(confirms*2 + extends*0.5 - challenges*2) / total`, normalised to 0-10

---

## Usage

```bash
pip install -r requirements.txt

# Try it offline with bundled sample data (no network or API key needed)
python -m claimaudit.cli "graphene batteries" --demo

# Audit a topic against live data from Semantic Scholar
python -m claimaudit.cli "graphene batteries"

# Fetch more papers, filter by year, and export a report
python -m claimaudit.cli "perovskite solar cells" --papers 20 --from-year 2015 --json report.json
```

Each claim is scored 0–10 from the balance of citing papers that confirm,
challenge, or extend it, with a verdict label (confirmed / well-supported /
mixed / contested / challenged).

### Live data and rate limits

Live queries use the Semantic Scholar API. Its free tier throttles
unauthenticated traffic heavily, so requests without a key are often
rate-limited. For live use, request a free API key from Semantic Scholar and
provide it via the `SEMANTIC_SCHOLAR_API_KEY` environment variable (or
`--api-key`). Without a key, use `--demo` to run against the bundled sample
data.

---

## Testing

Install the dependencies and run the suite:

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt pytest   # Linux/macOS: .venv/bin/pip
.venv/Scripts/python -m pytest -v
```

Exercise the CLI directly with `python -m claimaudit.cli --help`.

---

## Project structure

```
claimaudit/
├── claimaudit/
│   ├── extractor.py    # regex-based claim extraction with Jaccard dedup
│   ├── scholar.py      # Semantic Scholar Graph API client
│   ├── matcher.py      # TF-IDF cosine similarity claim-to-context matching
│   ├── classifier.py   # confirms/challenges/extends/neutral classification
│   ├── scorer.py       # survival score computation and verdict thresholds
│   ├── reporter.py     # HTML and JSON output
│   └── cli.py
└── tests/
    ├── test_classifier.py
    └── test_scorer.py
```

---

## Stack

Python 3.10, PyMuPDF, scikit-learn, Requests, Typer, Rich

No API key required. Semantic Scholar is publicly accessible.
