# Sermon Search

Full-stack PDF sermon indexing and search application with AI-powered semantic search and a data migration pipeline.

## Overview

Sermon Search ingests PDF sermon files, chunks and indexes them using vector embeddings, then lets users search by natural language query through a React web UI. A Python migration script imports existing sermon data from a remote SQLite database into SQL Server.

## Tech Stack

**Backend:** ASP.NET Core 8 · C# · Entity Framework Core  
**Frontend:** React · TypeScript  
**Database:** SQL Server  
**Migration:** Python · paramiko · pyodbc  
**Auth:** JWT  

## Features

- PDF upload and automatic chunking
- AI semantic search over sermon text
- Admin interface for PDF management
- Mobile-friendly PDF reader API
- Data migration from remote SQLite source

## Getting Started

### Prerequisites
- [.NET 8 SDK](https://dotnet.microsoft.com/download)
- SQL Server (Express or Developer edition)
- Node.js 18+
- ODBC Driver 17 for SQL Server (for migration script)

### API

```bash
cd api
cp appsettings.Example.json appsettings.json   # fill in your connection string and API key
dotnet ef database update
dotnet run
# API runs at https://localhost:5001
```

### Web UI

```bash
cd web
npm install
npm run dev
# Opens at http://localhost:5173
```

### Data Migration

```bash
cd ..   # repo root
cp .env.example .env   # fill in SSH and SQL Server credentials
pip install paramiko pyodbc python-dotenv
python migrate.py
```

## Project Structure

```
api/          # ASP.NET Core 8 REST API
web/          # React + TypeScript frontend
migrate.py    # SQLite → SQL Server migration script
.env.example  # Environment variable template
```

## License

MIT
