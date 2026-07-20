"""ClaimAudit CLI — audit research claims via Semantic Scholar."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from claimaudit.classifier import ClaimClassifier
from claimaudit.reporter import render_html, render_text, render_json

app     = typer.Typer(name="claimaudit", add_completion=False)
console = Console()


@app.command("audit")
def audit(
    topic: str = typer.Argument(..., help="Research topic to audit"),
    n_papers: int     = typer.Option(10,   "--papers",    "-n"),
    from_year: int    = typer.Option(2000, "--from-year", "-f"),
    to_year: int      = typer.Option(2025, "--to-year",   "-t"),
    min_citations: int= typer.Option(5,    "--min-cites"),
    html_out: Path    = typer.Option(None, "--html"),
    json_out: Path    = typer.Option(None, "--json"),
    api_key: str      = typer.Option("",   "--api-key", envvar="S2_API_KEY"),
):
    """Audit scientific claims in papers about a topic."""
    console.print(f"[bold]Auditing:[/bold] {topic!r} — fetching up to {n_papers} papers…")

    clf     = ClaimClassifier(api_key=api_key, min_citations=min_citations)
    results = clf.audit_topic(topic, n_papers, from_year, to_year)

    if not results:
        console.print("[yellow]No auditable claims found.[/yellow]")
        raise typer.Exit()

    table = Table(title=f"ClaimAudit: {topic}")
    table.add_column("Score", justify="right")
    table.add_column("Verdict")
    table.add_column("Paper")
    table.add_column("Claim (truncated)")
    for r in results:
        s = r.survival
        table.add_row(
            f"{s.score}/10",
            s.verdict,
            r.paper.title[:50],
            s.claim_text[:60] + "…",
        )
    console.print(table)

    if html_out:
        render_html(results, output_path=html_out)
        console.print(f"HTML -> {html_out}")
    if json_out:
        json_out.write_text(render_json(results))
        console.print(f"JSON -> {json_out}")


if __name__ == "__main__":
    app()
