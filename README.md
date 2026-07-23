# ClaimAudit

Tracks how well the empirical claims in a research paper hold up over time. Given a research topic, it searches Semantic Scholar, extracts quantitative and causal claims from paper abstracts, finds the citing papers, and classifies each citation as confirming, challenging, or extending the original claim. The result is a per-claim survival report.

Claim extraction and citation classification are rule-based, using signal-word and marker-phrase patterns rather than a trained model. Built to explore text pipelines on academic writing and to think about how scientific consensus forms (or doesn't) after publication.

---

## How it works

1. Claims are extracted from paper abstracts using regex signal patterns for quantitative, comparative, and causal language
2. Citing papers, and the context text of each citation, are retrieved from Semantic Scholar
3. Each citation context is classified as confirms / challenges / extends / neutral using marker-phrase patterns
4. A survival score (0–10) is computed per claim from the balance of confirming and challenging citations; extending citations add a small bounded bonus and neutral citations pull the score toward the midpoint

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
│   ├── extractor.py    # regex-based claim extraction from abstracts
│   ├── scholar.py      # Semantic Scholar Graph API client (+ demo data)
│   ├── matcher.py      # citation-relation classification (confirms/challenges/extends)
│   ├── classifier.py   # audit pipeline: search, extract, classify, score
│   ├── scorer.py       # survival score computation and verdict thresholds
│   ├── reporter.py     # HTML and JSON output
│   ├── demo_data.py    # bundled sample data for --demo
│   └── cli.py
└── tests/
    ├── test_classifier.py
    └── test_scorer.py
```

---

## Stack

Python 3.10, Requests, Typer, Rich. No third-party ML or PDF libraries;
claim extraction and citation classification are rule-based.

An API key is optional but recommended: Semantic Scholar's free tier throttles
unauthenticated traffic, so live runs without a key are often rate-limited.
Use `--demo` to run offline against the bundled sample data.
