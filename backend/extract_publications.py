import xml.etree.ElementTree as ET
import json
from database import (
    create_tables,
    get_publication,
    save_publication,
    get_all_publications,
)
from flask import Flask, Response, stream_with_context, jsonify, request
from flask_cors import CORS
import requests
from ai_summarizer import summarize_abstract
from clinical_trials import search_trials

app = Flask(__name__)
CORS(app)

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

create_tables()


def get_latest_publications():

    search_response = requests.get(
        f"{BASE_URL}/esearch.fcgi",
        params={
            "db": "pubmed",
            "term": "\"O'Bryant SE\"[Author]",
            "retmode": "json",
            "retmax": 20,
            "sort": "pub date",
        },
        timeout=10,
    )

    search_response.raise_for_status()

    ids = search_response.json()["esearchresult"]["idlist"]

    if not ids:
        return

    fetch_response = requests.get(
        f"{BASE_URL}/efetch.fcgi",
        params={
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "xml",
        },
        timeout=10,
    )

    fetch_response.raise_for_status()

    root = ET.fromstring(fetch_response.text)

    for article in root.findall(".//PubmedArticle"):

        pmid = article.findtext(".//PMID")

        title_element = article.find(".//ArticleTitle")

        title = (
            "".join(title_element.itertext())
            if title_element is not None
            else "No title"
        )

        journal = (
            article.findtext(".//Journal/Title")
            or "Unknown journal"
        )

        year = (
            article.findtext(".//PubDate/Year")
            or article.findtext(".//ArticleDate/Year")
            or ""
        )

        month = (
            article.findtext(".//PubDate/Month")
            or article.findtext(".//ArticleDate/Month")
            or ""
        )

        day = (
            article.findtext(".//PubDate/Day")
            or article.findtext(".//ArticleDate/Day")
            or ""
        )

        publication_date = f"{year}-{month}-{day}"

        authors = []

        for author in article.findall(".//Author"):

            first = author.findtext("ForeName")
            last = author.findtext("LastName")

            if first and last:
                authors.append(f"{first} {last}")

        abstract_elements = article.findall(
            ".//Abstract/AbstractText"
        )

        abstract = " ".join(
            "".join(element.itertext())
            for element in abstract_elements
        )

        # Summary
        
        existing = get_publication(pmid)

        if existing is not None:
            summary = existing["lay_summary"]
            print(f"Using cached publication for PMID {pmid}")
        else:
            summary = summarize_abstract(title, abstract)
            print(f"Generating summary for PMID {pmid}")


        publication = {

            "pmid": pmid,
            "title": title,
            "journal": journal,
            "year": year,
            "date": publication_date,
            "authors": authors,
            "abstract": abstract,
            "summary": summary,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        }
        save_publication(publication)

        print(f"Processed publication: {pmid} - {title}")
        print("---------------------------------------------------------------")

        # Enviar inmediatamente esta publicación
        yield publication



@app.route("/api/publications")
def publications():

    def generate():
        try:
            for publication in get_latest_publications():
                yield json.dumps(publication) + "\n"

        except Exception as e:
            yield json.dumps({
                "error": str(e)
            }) + "\n"

    return Response(
        stream_with_context(generate()),
        mimetype="application/x-ndjson",
    )


# @app.route("/api/publications/update", methods=["POST"])
# def update_publications():

#     try:
#         count = 0

#         for publication in get_latest_publications():
#             count += 1

#         return {
#             "message": "Publications updated",
#             "count": count,
#         }

#     except Exception as e:
#         return {
#             "error": str(e)
#         }, 500



@app.route("/api/trials/search")
def trial_search():
    query = request.args.get("q", "").strip()
    if not query:

        return jsonify({
            "error": "Search query is required"
        }), 400

    try:
        trials = search_trials(query)
        return jsonify(trials)

    except Exception as error:
        print(error)

        return jsonify({
            "error": "Could not retrieve clinical trials"
        }), 500
    

if __name__ == "__main__":
    app.run(debug=True, port=5001)