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

# Audit a paper by DOI
python -m claimaudit.cli audit --doi 10.1038/s41586-021-03819-2

# Limit citation depth and export JSON
python -m claimaudit.cli audit --doi 10.1038/nature12373 --max-citations 100 --json report.json
```

Output is an HTML report with a stacked bar chart per claim and a verdict label (Robust / Supported / Mixed / Contested / Disputed).

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
