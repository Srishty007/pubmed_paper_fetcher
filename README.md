# 🧪 PubMed Paper Fetcher

A Python CLI tool that fetches PubMed research papers based on a user-defined query and filters results to identify papers authored by pharmaceutical or biotech companies. Outputs results in CSV format.

---

## ✅ Features

- 🔍 Search PubMed using full query syntax (e.g., `"covid-19 AND cancer"`)
- 🧬 Filters for **non-academic authors** and **biotech/pharma affiliations**
- 📄 Exports data to CSV
- ⚙️ CLI options: debug logging, output to file
- 🔁 Clean, modular code with Poetry packaging
- 📦 Published to [TestPyPI](https://test.pypi.org/project/pubmed-paper-fetcher-srishty007/)

---

## 📁 Project Structure

```

pubmed\_paper\_fetcher/
├── src/
│   └── pubmed\_paper\_fetcher/
│       ├── **init**.py
│       ├── cli.py              # CLI entrypoint (Typer)
│       └── core.py             # Core logic (PubMed API, filtering)
├── tests/                      # Optional (for future test cases)
├── pyproject.toml              # Poetry config
├── README.md                   # Project documentation

````

---

## 💻 Installation

1. Clone the repository:

```bash
git clone https://github.com/Srishty007/pubmed_paper_fetcher.git
cd pubmed_paper_fetcher
````

2. Install dependencies using [Poetry](https://python-poetry.org/):

```bash
poetry install
```

---

## 🚀 Usage

### Run via Poetry:

```bash
poetry run get-papers-list "covid-19 AND cancer" --file results.csv --debug
```

### Options:

| Flag          | Description                                |
| ------------- | ------------------------------------------ |
| `<query>`     | Required. The PubMed search query          |
| `-f, --file`  | (Optional) Filename to save results as CSV |
| `-d, --debug` | (Optional) Enable debug output to console  |
| `-h, --help`  | Show help message and usage instructions   |

---

## 🧪 Install from TestPyPI (optional)

```bash
pip install -i https://test.pypi.org/simple/ pubmed-paper-fetcher-srishty007
```

Then run:

```bash
get-papers-list "cancer" --file test.csv --debug
```

---

## 🏢 Heuristics for Non-Academic Author Detection

We use simple rules such as:

* Affiliation **not** containing keywords like `university`, `institute`, `college`, `hospital`, etc.
* Email domain not ending in `.edu`, `.ac`, or `.org`
* Custom keywords like `Inc`, `Ltd`, `Pharma`, `Biotech`, etc.

You can adjust this logic in `core.py`.

---

## 🧠 Tools Used

* [Python Typer](https://typer.tiangolo.com/) – CLI interface
* [Biopython Entrez](https://biopython.org/wiki/Entrez) – PubMed API
* [Poetry](https://python-poetry.org/) – Dependency and packaging manager
* [ChatGPT (LLM)](https://openai.com/chatgpt) – Assisted with planning, CLI design, and packaging

---

## 🧪 Test Output Preview

Example CSV columns:

* PubmedID
* Title
* Publication Date
* Non-academic Author(s)
* Company Affiliation(s)
* Corresponding Author Email

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙋‍♀️ Author

Built with ❤️ by **Srishty007**
🔗 GitHub: [github.com/Srishty007](https://github.com/Srishty007)

---

```

---
