"""Bundled sample data for offline demo mode.

These are illustrative records, not live results from Semantic Scholar. They let
the tool run end to end without network access or an API key, which is useful
for a quick demonstration and for tests. Pass --demo on the CLI to use them.
"""

from __future__ import annotations

from claimaudit.scholar import Author, CitationContext, Paper

_PAPERS = [
    Paper(
        paper_id="demo-a",
        title="Graphene anodes triple lithium-ion battery capacity",
        abstract=(
            "We show that a graphene-coated anode increases lithium-ion battery "
            "capacity by a factor of three. The results demonstrate stable "
            "performance over 500 charge cycles."
        ),
        year=2015,
        authors=[Author("A. Meyer"), Author("D. Fischer")],
        citation_count=210,
    ),
    Paper(
        paper_id="demo-b",
        title="A perovskite solar cell exceeding 25% efficiency",
        abstract=(
            "We report that a mixed-cation perovskite achieves a power conversion "
            "efficiency above 25%. We find that trace additives suppress ion "
            "migration and improve stability."
        ),
        year=2018,
        authors=[Author("P. Sharma")],
        citation_count=160,
    ),
    Paper(
        paper_id="demo-c",
        title="Room-temperature superconductivity in a hydride at ambient pressure",
        abstract=(
            "We demonstrate that a novel hydride superconducts at room temperature "
            "and ambient pressure. This result suggests a route to lossless power "
            "transmission."
        ),
        year=2021,
        authors=[Author("N. Volkov"), Author("R. Iqbal")],
        citation_count=90,
    ),
]

# Citation contexts keyed by paper id, mixing confirming, challenging,
# extending, and background language so the survival scores differ.
def _ctx(pid, title, year, text, influential=False, intents=("result",)):
    return CitationContext(pid, title, year, list(intents), influential, text)


# demo-a is largely confirmed, demo-b is genuinely mixed, and demo-c is
# widely challenged, so the survival verdicts differ across the three.
_CITATIONS: dict[str, list[CitationContext]] = {
    "demo-a": [
        _ctx("demo-a1", "Scalable graphene anode manufacturing", 2017,
             "we confirm the threefold capacity gain reported by Meyer et al.", True),
        _ctx("demo-a2", "Long-cycle graphene electrodes", 2018,
             "our measurements are consistent with their findings"),
        _ctx("demo-a3", "High-rate graphene anodes", 2018,
             "these results support the reported capacity improvement"),
        _ctx("demo-a4", "Graphene anodes revisited", 2019,
             "we build on this work to reach 700 cycles"),
        _ctx("demo-a5", "Commercial cell integration", 2020,
             "consistent with Meyer et al., we observe stable cycling"),
        _ctx("demo-a6", "A cautionary replication", 2021,
             "we could not replicate the capacity and our data contradict it"),
    ],
    "demo-b": [
        _ctx("demo-b1", "Additive engineering in perovskites", 2019,
             "as previously reported (Sharma, 2018)", False, ("background",)),
        _ctx("demo-b2", "Confirmatory efficiency study", 2019,
             "we confirm efficiencies above 25% under the same protocol"),
        _ctx("demo-b3", "Independent certification", 2020,
             "our certified measurement agrees with the reported value"),
        _ctx("demo-b4", "Perovskite stability challenges", 2020,
             "our results are inconsistent with the stability claimed"),
        _ctx("demo-b5", "Ion migration in mixed cations", 2021,
             "this contradicts the suppression mechanism proposed there", True),
        _ctx("demo-b6", "Long-term degradation", 2022,
             "we dispute the durability claim; cells failed within weeks"),
    ],
    "demo-c": [
        _ctx("demo-c1", "Scrutinising ambient superconductivity", 2022,
             "we dispute these claims; independent measurements do not support them", True),
        _ctx("demo-c2", "Reanalysis of hydride data", 2022,
             "the reported transition could not be reproduced and appears inconsistent"),
        _ctx("demo-c3", "Failed replication at ambient pressure", 2023,
             "we refute the ambient-pressure result"),
        _ctx("demo-c4", "Magnetic susceptibility revisited", 2023,
             "these findings contradict the superconducting claim"),
        _ctx("demo-c5", "Community replication effort", 2023,
             "no group could replicate the effect, inconsistent with the original"),
        _ctx("demo-c6", "A background citation", 2023,
             "for context see the original hydride report", False, ("background",)),
    ],
}


def demo_search(query: str, limit: int = 10) -> list[Paper]:
    """Return the sample papers, ignoring the query text."""
    return _PAPERS[:limit]


def demo_citations(paper_id: str, limit: int = 50) -> list[CitationContext]:
    return list(_CITATIONS.get(paper_id, []))[:limit]
