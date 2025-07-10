import typer
from typing import Optional
from .core import fetch_pubmed_ids, fetch_paper_details
import pandas as pd

app = typer.Typer()

@app.command()
def main(
    query: str = typer.Argument(..., help="PubMed search query"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="File name to save results as CSV"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug logging")
):
    if debug:
        typer.echo(f"Searching PubMed for: {query}")

    ids = fetch_pubmed_ids(query)
    if debug:
        typer.echo(f"Found {len(ids)} paper IDs: {ids}")

    papers = fetch_paper_details(ids)

    results = []
    for paper in papers:
        results.append({
            "PubmedID": paper.pubmed_id,
            "Title": paper.title,
            "Publication Date": paper.publication_date,
            "Non-academic Author(s)": "; ".join(paper.non_academic_authors),
            "Company Affiliation(s)": "; ".join(paper.company_affiliations),
            "Corresponding Author Email": paper.corresponding_email
        })

    df = pd.DataFrame(results)

    if file:
        df.to_csv(file, index=False)
        typer.echo(f"Saved {len(df)} results to {file}")
    else:
        typer.echo(df.to_string(index=False))


if __name__ == "__main__":
    app()
