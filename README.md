# UK Job Market Data Pipeline

An end-to-end Azure data engineering pipeline that ingests, transforms, and visualises UK job market data from multiple sources.

## Architecture
Raw Layer (ADLS Gen2)     Transformation          Warehouse Layer        Visualisation
─────────────────────     ──────────────          ───────────────        ─────────────
Kaggle LinkedIn CSV   →   Databricks          →   Star Schema        →   Power BI
Reed API (live)           PySpark/Pandas          fact_jobs              Dashboard
Adzuna API (live)         Cleaning                dim_employer
Enrichment              dim_location
dim_date
## Tech Stack

- **Cloud**: Microsoft Azure
- **Data Lake**: Azure Data Lake Storage Gen2
- **Orchestration**: Azure Data Factory
- **Processing**: Azure Databricks (PySpark)
- **Warehouse**: Azure Synapse Analytics
- **Visualisation**: Power BI
- **Ingestion**: Python, Requests, Azure Storage SDK
- **Languages**: Python, SQL

## Data Sources

- **Kaggle**: 1.3M LinkedIn job postings (historical)
- **Reed API**: Live UK job listings (400+ daily)
- **Adzuna API**: Live UK job listings (250+ daily)

## Pipeline Stages

### 1. Ingestion
- Kaggle dataset uploaded to ADLS Gen2 raw container
- Reed API pulls jobs by keyword and uploads JSON to raw/reed/
- Adzuna API pulls jobs by keyword and uploads JSON to raw/adzuna/

### 2. Transformation (Databricks)
- Load raw JSON from ADLS Gen2
- Clean and standardise column names
- Fill null values
- Add derived columns: salary_band, visa_sponsorship flag, experience_level
- Combine Reed + Adzuna into unified dataset
- Save to cleaned container

### 3. Star Schema Modelling
- fact_jobs: 648 rows, 15 columns
- dim_employer: 217 unique employers
- dim_location: 138 unique locations
- dim_date: 287 unique dates
- Save to warehouse container

### 4. Visualisation (Power BI)
- Total Jobs KPI card
- Jobs by Location (bar chart)
- Salary Distribution (pie chart)
- Experience Levels (bar chart)
- Source Comparison Reed vs Adzuna (pie chart)

## Key Insights

- 648 live UK tech jobs analysed
- Manchester is the top hiring location (232 jobs)
- 40k-60k is the most common salary band (25%)
- Mid-level roles dominate (265 out of 648)
- Reed contributes 61% of jobs, Adzuna 39%
- 2 jobs explicitly mention visa sponsorship

## Setup

1. Clone the repo
2. Copy config/config_template.py to config/config.py
3. Fill in your Azure, Reed and Adzuna credentials
4. Install dependencies: pip install -r requirements.txt
5. Run ingestion scripts in order:
   - python ingestion/upload_kaggle.py
   - python ingestion/reed_ingest.py
   - python ingestion/adzuna_ingest.py

## Project Structure
uk-job-market-pipeline/
├── config/
│   └── config_template.py
├── ingestion/
│   ├── upload_kaggle.py
│   ├── reed_ingest.py
│   └── adzuna_ingest.py
├── transformation/
├── scripts/
├── requirements.txt
└── README.md
## Author

Kalpana Joyce Dovari
MSc Artificial Intelligence — Northumbria University London
[Portfolio](https://my-portfolio-taupe-kappa-13.vercel.app) | [LinkedIn](https://linkedin.com/in/kalpanajoycedovari) | [GitHub](https://github.com/kalpanajoycedovari)