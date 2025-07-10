from typing import List, Dict
import requests
import xmltodict
from dataclasses import dataclass
import re


@dataclass
class Paper:
    pubmed_id: str
    title: str
    publication_date: str
    non_academic_authors: List[str]
    company_affiliations: List[str]
    corresponding_email: str


def fetch_pubmed_ids(query: str, max_results: int = 20) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_paper_details(ids: List[str]) -> List[Paper]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    id_string = ",".join(ids)
    params = {
        "db": "pubmed",
        "id": id_string,
        "retmode": "xml"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    xml_data = xmltodict.parse(response.content)

    papers = []
    articles = xml_data.get("PubmedArticleSet", {}).get("PubmedArticle", [])

    if isinstance(articles, dict):
        articles = [articles]

    for article in articles:
        try:
            medline = article.get("MedlineCitation", {})
            article_data = medline.get("Article", {})
            pubmed_id = medline.get("PMID", {}).get("#text", "N/A")
            title = article_data.get("ArticleTitle", "N/A")
            pub_date = article_data.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {}).get("Year", "N/A")
            authors = article_data.get("AuthorList", {}).get("Author", [])

            non_academic_authors = []
            company_affiliations = []
            email = ""

            if isinstance(authors, dict):
                authors = [authors]

            for author in authors:
                affil_info = author.get("AffiliationInfo", [])
                if isinstance(affil_info, dict):
                    affil_info = [affil_info]
                for aff in affil_info:
                    aff_text = aff.get("Affiliation", "")
                    if aff_text:
                        if is_non_academic(aff_text):
                            name = " ".join(filter(None, [author.get("ForeName", ""), author.get("LastName", "")]))
                            non_academic_authors.append(name)
                            company_affiliations.append(aff_text)

                        found_email = extract_email(aff_text)
                        if found_email:
                            email = found_email

            papers.append(Paper(
                pubmed_id=pubmed_id,
                title=title,
                publication_date=pub_date,
                non_academic_authors=non_academic_authors,
                company_affiliations=company_affiliations,
                corresponding_email=email
            ))
        except Exception as e:
            print(f"Error parsing article: {e}")

    return papers


def is_non_academic(affiliation: str) -> bool:
    academic_keywords = ["university", "college", "institute", "hospital", "school", "department"]
    return not any(keyword.lower() in affiliation.lower() for keyword in academic_keywords)


def extract_email(text: str) -> str:
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else ""
