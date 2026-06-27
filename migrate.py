"""
migrate.py — Copy PdfDocuments + PdfChunks from SQLite on the remote server
into local SQL Server (SermonSearch database).

Prerequisites:
  - pip install paramiko pyodbc python-dotenv
  - ODBC Driver 17 or 18 for SQL Server installed locally
  - SermonSearch DB already created (run: dotnet ef database update in api/)
  - Server SSH access
  - Copy .env.example to .env and fill in your credentials
"""

import os
import paramiko
import pyodbc
import io
import csv
from dotenv import load_dotenv

load_dotenv()

SSH_HOST = os.environ["SSH_HOST"]
SSH_PORT = int(os.environ.get("SSH_PORT", "22"))
SSH_USER = os.environ["SSH_USER"]
SSH_PASS = os.environ["SSH_PASS"]

SQL_SERVER = os.environ["SQL_SERVER"]
SQL_DB = os.environ.get("SQL_DB", "SermonSearch")
SQL_USER = os.environ["SQL_USER"]
SQL_PASS = os.environ["SQL_PASS"]


def fetch_sqlite(ssh, query):
    stdin, stdout, stderr = ssh.exec_command(
        f'sqlite3 -csv /var/www/sermon-search/sermons.db "{query}"'
    )
    return list(csv.reader(io.StringIO(stdout.read().decode())))


def main():
    print("Connecting to SSH...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)

    print("Connecting to SQL Server...")
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DB};"
        f"UID={SQL_USER};"
        f"PWD={SQL_PASS}"
    )
    cursor = conn.cursor()

    # Check existing counts
    cursor.execute("SELECT COUNT(*) FROM PdfDocuments")
    existing_docs = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM PdfChunks")
    existing_chunks = cursor.fetchone()[0]
    print(f"Existing: {existing_docs} docs, {existing_chunks} chunks")

    # Fetch PdfDocuments from SQLite
    print("Fetching PdfDocuments from SQLite...")
    rows = fetch_sqlite(ssh, "SELECT Id, FileName, Title, Author, Year, PageCount, UploadedAt FROM PdfDocuments")
    doc_id_map = {}  # old SQLite ID -> new SQL Server ID

    inserted_docs = 0
    for row in rows:
        if not row:
            continue
        old_id, file_name, title, author, year, page_count, uploaded_at = row

        # Skip if already exists
        cursor.execute("SELECT Id FROM PdfDocuments WHERE FileName = ?", file_name)
        existing = cursor.fetchone()
        if existing:
            doc_id_map[old_id] = existing[0]
            continue

        cursor.execute(
            "INSERT INTO PdfDocuments (FileName, Title, Author, Year, PageCount, UploadedAt) "
            "OUTPUT INSERTED.Id VALUES (?, ?, ?, ?, ?, ?)",
            file_name, title, author,
            int(year) if year else None,
            int(page_count) if page_count else None,
            uploaded_at
        )
        new_id = cursor.fetchone()[0]
        doc_id_map[old_id] = new_id
        inserted_docs += 1

    conn.commit()
    print(f"Inserted {inserted_docs} PdfDocuments")

    # Fetch PdfChunks from SQLite (only for indexed docs)
    print("Fetching PdfChunks from SQLite...")
    rows = fetch_sqlite(ssh, "SELECT Id, DocumentId, ChunkIndex, Text, Embedding FROM PdfChunks")

    inserted_chunks = 0
    for row in rows:
        if not row:
            continue
        old_chunk_id, old_doc_id, chunk_index, text, embedding = row

        new_doc_id = doc_id_map.get(old_doc_id)
        if not new_doc_id:
            continue

        # Skip if already exists
        cursor.execute(
            "SELECT Id FROM PdfChunks WHERE DocumentId = ? AND ChunkIndex = ?",
            new_doc_id, int(chunk_index)
        )
        if cursor.fetchone():
            continue

        cursor.execute(
            "INSERT INTO PdfChunks (DocumentId, ChunkIndex, Text, Embedding) VALUES (?, ?, ?, ?)",
            new_doc_id, int(chunk_index), text, embedding
        )
        inserted_chunks += 1

    conn.commit()
    print(f"Inserted {inserted_chunks} PdfChunks")

    cursor.close()
    conn.close()
    ssh.close()
    print("Migration complete.")


if __name__ == "__main__":
    main()
