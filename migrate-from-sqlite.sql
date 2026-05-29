-- Migration script: SQLite (caclouky.db) → SQL Server (SermonSearch)
-- Run this ONCE after creating the SermonSearch database via EF migrations.
-- Safe to inspect and verify before running — does NOT drop any existing data.

-- Step 1: Export from SQLite on the server (run via SSH):
--   sqlite3 ~/caclouky/caclouky.db ".mode csv" ".headers on" ".output /tmp/pdf_documents.csv" "SELECT * FROM PdfDocuments;" ".output /tmp/pdf_chunks.csv" "SELECT * FROM PdfChunks;"

-- Step 2: Import CSVs into SQL Server using SSMS Import Wizard or BCP.
--   Or use the Python migration script: migrate.py (see below)

-- Verify row counts after migration:
SELECT 'PdfDocuments' AS [Table], COUNT(*) AS [Rows] FROM PdfDocuments
UNION ALL
SELECT 'PdfChunks',               COUNT(*)        FROM PdfChunks;
