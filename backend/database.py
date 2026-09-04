import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).with_name("publications.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS publications (
                pmid TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                journal TEXT,
                year TEXT,
                authors TEXT,
                abstract TEXT,
                lay_summary TEXT,
                url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def get_publication(pmid):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT *
            FROM publications
            WHERE pmid = ?
            """,
            (pmid,),
        ).fetchone()

    if row is None:
        return None

    publication = dict(row)

    publication["authors"] = json.loads(
        publication["authors"] or "[]"
    )

    return publication


def save_publication(publication):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO publications (
                pmid,
                title,
                journal,
                year,
                authors,
                abstract,
                lay_summary,
                url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(pmid) DO UPDATE SET
                title = excluded.title,
                journal = excluded.journal,
                year = excluded.year,
                authors = excluded.authors,
                abstract = excluded.abstract,
                lay_summary = excluded.lay_summary,
                url = excluded.url,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                publication["pmid"],
                publication["title"],
                publication["journal"],
                publication["year"],
                json.dumps(publication["authors"]),
                publication["abstract"],
                publication["summary"],
                publication["url"],
            ),
        )


def get_all_publications():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM publications
            ORDER BY created_at DESC
            """
        ).fetchall()

    publications = []

    for row in rows:
        publication = dict(row)

        publication["authors"] = json.loads(
            publication["authors"] or "[]"
        )

        publication["summary"] = publication.pop(
            "lay_summary"
        )

        publications.append(publication)

    return publications