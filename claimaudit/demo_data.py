"""Bundled sample records for offline demo mode.

These are illustrative, not live results from Semantic Scholar. They let the
tool run end to end without network access or an API key, which is useful for a
quick demonstration and for tests. Pass --demo on the CLI to use them.

The records are plain dictionaries in the same shape the Semantic Scholar API
returns, and this module imports nothing from the rest of the package. That is
deliberate: an earlier version defined them as Paper and CitationContext
objects, which meant importing those classes from scholar.py while scholar.py
imported this module back. The cycle only worked because one side deferred its
import inside a function, and would have broken the moment anyone moved it to
the top of the file. Keeping the data as dictionaries lets the dependency run
one way, from scholar.py to here.
"""

from __future__ import annotations

PAPERS: list[dict] = [
    {
        "paperId": "demo-a",
        "title": "Graphene anodes triple lithium-ion battery capacity",
        "abstract": (
            "We show that a graphene-coated anode increases lithium-ion battery "
            "capacity by a factor of three. The results demonstrate stable "
            "performance over 500 charge cycles."
        ),
        "year": 2015,
        "authors": [{"name": "A. Meyer"}, {"name": "D. Fischer"}],
        "citationCount": 210,
    },
    {
        "paperId": "demo-b",
        "title": "A perovskite solar cell exceeding 25% efficiency",
        "abstract": (
            "We report that a mixed-cation perovskite achieves a power conversion "
            "efficiency above 25%. We find that trace additives suppress ion "
            "migration and improve stability."
        ),
        "year": 2018,
        "authors": [{"name": "P. Sharma"}],
        "citationCount": 160,
    },
    {
        "paperId": "demo-c",
        "title": "Room-temperature superconductivity in a hydride at ambient pressure",
        "abstract": (
            "We demonstrate that a novel hydride superconducts at room temperature "
            "and ambient pressure. This result suggests a route to lossless power "
            "transmission."
        ),
        "year": 2021,
        "authors": [{"name": "N. Volkov"}, {"name": "R. Iqbal"}],
        "citationCount": 90,
    },
]


def _citation(paper_id: str, title: str, year: int, text: str,
              influential: bool = False, intents: tuple[str, ...] = ("result",)) -> dict:
    return {
        "citingPaper": {"paperId": paper_id, "title": title, "year": year},
        "intents": list(intents),
        "isInfluential": influential,
        "contexts": [text],
    }


# demo-a is largely confirmed, demo-b is genuinely mixed, and demo-c is widely
# challenged, so the three survival verdicts differ.
CITATIONS: dict[str, list[dict]] = {
    "demo-a": [
        _citation("demo-a1", "Scalable graphene anode manufacturing", 2017,
                  "we confirm the threefold capacity gain reported by Meyer et al.", True),
        _citation("demo-a2", "Long-cycle graphene electrodes", 2018,
                  "our measurements are consistent with their findings"),
        _citation("demo-a3", "High-rate graphene anodes", 2018,
                  "these results support the reported capacity improvement"),
        _citation("demo-a4", "Graphene anodes revisited", 2019,
                  "we build on this work to reach 700 cycles"),
        _citation("demo-a5", "Commercial cell integration", 2020,
                  "consistent with Meyer et al., we observe stable cycling"),
        _citation("demo-a6", "A cautionary replication", 2021,
                  "we could not replicate the capacity and our data contradict it"),
    ],
    "demo-b": [
        _citation("demo-b1", "Additive engineering in perovskites", 2019,
                  "as previously reported (Sharma, 2018)", False, ("background",)),
        _citation("demo-b2", "Confirmatory efficiency study", 2019,
                  "we confirm efficiencies above 25% under the same protocol"),
        _citation("demo-b3", "Independent certification", 2020,
                  "our certified measurement agrees with the reported value"),
        _citation("demo-b4", "Perovskite stability challenges", 2020,
                  "our results are inconsistent with the stability claimed"),
        _citation("demo-b5", "Ion migration in mixed cations", 2021,
                  "this contradicts the suppression mechanism proposed there", True),
        _citation("demo-b6", "Long-term degradation", 2022,
                  "we dispute the durability claim; cells failed within weeks"),
    ],
    "demo-c": [
        _citation("demo-c1", "Scrutinising ambient superconductivity", 2022,
                  "we dispute these claims; independent measurements do not support them", True),
        _citation("demo-c2", "Reanalysis of hydride data", 2022,
                  "the reported transition could not be reproduced and appears inconsistent"),
        _citation("demo-c3", "Failed replication at ambient pressure", 2023,
                  "we refute the ambient-pressure result"),
        _citation("demo-c4", "Magnetic susceptibility revisited", 2023,
                  "these findings contradict the superconducting claim"),
        _citation("demo-c5", "Community replication effort", 2023,
                  "no group could replicate the effect, inconsistent with the original"),
        _citation("demo-c6", "A background citation", 2023,
                  "for context see the original hydride report", False, ("background",)),
    ],
}


def search_response(limit: int = 10) -> dict:
    """Return sample papers shaped like the paper/search endpoint."""
    return {"data": PAPERS[:limit]}


def citations_response(paper_id: str, limit: int = 50) -> dict:
    """Return sample citations shaped like the paper/{id}/citations endpoint."""
    return {"data": CITATIONS.get(paper_id, [])[:limit]}
