# 🌱 Paris Shared Gardens - ETL Analysis

Analysis of shared gardens distribution across Paris using OpenData Paris API.


##  Quick Start

```bash
# Clone and configure
git clone [your-repo]
cd OpenData-DevOps

# Start everything
docker-compose up -d

# Access dashboard
open http://localhost:8081/
```

##  Available Services

- **HTML Dashboard:** http://localhost:8081/ 
- **Metabase:** http://localhost:3001/ 


##  Architecture

```
OpenData API → Python ETL → PostgreSQL → Analyzer → Dashboard/Metabase
```

## Project Structure

```
OpenData-DevOps/
├── python/
│   ├── etl/
│   │   ├── fetch_data.py    # API extraction
│   │   └── load_db.py       # Database loading
│   ├── main.py              # ETL orchestration
│   ├── analyzer.py          # Data analysis
│   └── requirements.txt
├── dashboard/
│   ├── index.html           # Web dashboard
│   └── server.py            # HTTP server
├── results/                 # JSON results
├── data/                    # Raw data
├── docker-compose.yml
├── Dockerfile
└── README.md
```

##  ETL Pipeline

1. **Extract:** OpenData Paris API (v2.1) with pagination
2. **Transform:** Validation, deduplication (MD5), cleaning
3. **Load:** PostgreSQL with batch insert and indexing
4. **Analyze:** Aggregations and JSON export

##  Docker Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| db | postgres:15-alpine | 5432 | Database |
| etl | Custom Python | - | ETL Pipeline + Analysis |
| dashboard | python:3.11-slim | 8081 | HTML Dashboard |
| metabase | metabase/metabase | 3001 | Advanced visualization |

## Useful Commands

```bash
# View logs
docker compose logs -f etl

# Check data
docker compose exec db psql -U app -d jardins -c "SELECT COUNT(*) FROM jardins_partages;"

# Restart ETL
docker compose restart etl

# View results
cat results/analysis.json
```


##  Tech Stack

- **Backend:** Python 3.11
- **Database:** PostgreSQL 15
- **Frontend:** HTML5 + Chart.js
- **Infrastructure:** Docker Compose
- **Source:** OpenData Paris


## Testing

```bash
# Full test
docker compose down -v && docker-compose up -d
docker compose logs etl | grep "SUCCESS"

# Database verification
docker compose exec db psql -U app -d jardins -c "SELECT arrondissement, COUNT(*) FROM jardins_partages GROUP BY arrondissement ORDER BY COUNT(*) DESC LIMIT 3;"
```

## 👤 Author

**Rihab Haddad**  
DevOps ETL Project 


---

