# SQL Question Answering — Day 4

## What is SQL QA?

SQL QA lets users ask questions in plain English and get answers from a structured database. The system converts the question to SQL, runs it safely, and summarizes the results in natural language using Groq LLM.

```
"How many customers are from each country?"
                    ↓
SELECT country, COUNT(*) FROM customers GROUP BY country LIMIT 100
                    ↓
        Query returned 20 rows
                    ↓
"There are 20 unique countries. The US has the most customers with 1,245..."
```

---

## The Full Flow

```
User question (plain English)
            │
            ▼
    ┌───────────────┐
    │ Schema Loader │  reads table names, columns, sample rows
    └───────┬───────┘
            │ schema text
            ▼
    ┌───────────────┐
    │ SQL Generator │  question + schema → Groq LLM → SQL query
    │  (Groq LLM)   │
    └───────┬───────┘
            │ raw SQL
            ▼
    ┌───────────────┐
    │   Validator   │  blocks DROP, DELETE, INSERT, UPDATE etc.
    └───────┬───────┘
            │ safe SQL
            ▼
    ┌───────────────┐
    │   Executor    │  runs SQL on SQLite database
    └───────┬───────┘
            │ rows + columns
            ▼
    ┌───────────────┐
    │  Summarizer   │  results + question → Groq LLM → plain English answer
    │  (Groq LLM)   │
    └───────┬───────┘
            │
            ▼
    Final answer to user
```

---

## The Four Components

### 1. Schema Loader (`utils/schema_loader.py`)
Reads the SQLite database and extracts table names, column names, data types, and 3 sample rows. This is passed to the LLM so it knows exactly what data exists before writing SQL. Without the schema, the LLM would guess column names and generate wrong queries.

### 2. SQL Generator (`generator/sql_generator.py`)
Sends the user question + schema to Groq's `llama-3.3-70b-versatile` model with a strict prompt — return SQL only, no explanations, no markdown. Temperature is set to 0 for deterministic output so the same question always generates the same SQL.

### 3. Validator + Executor (`pipelines/sql_pipeline.py`)
Two steps in one:
- **Validator** — blocks any SQL containing `DROP`, `DELETE`, `INSERT`, `UPDATE`, `ALTER`, `CREATE`, `TRUNCATE`. Only `SELECT` queries are allowed. This prevents the LLM from accidentally destroying your data.
- **Executor** — runs the validated SQL on SQLite and returns rows and column names.

### 4. Summarizer (`pipelines/sql_pipeline.py`)
Takes the raw query results (up to 20 rows) and passes them back to Groq with the original question. The LLM writes a clear, specific answer mentioning actual numbers and names from the data.

---

## Files

```
src/
├── utils/
│   ├── create_db.py          # one-time script to create SQLite from CSV
│   └── schema_loader.py      # reads table structure from DB
├── generator/
│   └── sql_generator.py      # question + schema → Groq → SQL
├── pipelines/
│   └── sql_pipeline.py       # validate → execute → summarize
└── data/
    └── sql/
        └── enterprise.db     # SQLite database (auto-created)
```

---

## Setup and Run

```bash
#  create database from CSV
python -m src.utils.create_db

# verify schema loads correctly
python -m src.utils.schema_loader

# test SQL generation alone
python -m src.generator.sql_generator

# run full pipeline
python -m src.pipelines.sql_pipeline
```

---

## Sample Questions and Generated SQL

| Question | Generated SQL |
|---|---|
| How many customers in total? | `SELECT COUNT(*) FROM customers` |
| Top 5 customers by age | `SELECT * FROM customers ORDER BY age DESC LIMIT 5` |
| How many customers per country? | `SELECT country, COUNT(*) FROM customers GROUP BY country` |
| Average age of customers | `SELECT AVG(age) FROM customers` |

---

## Safety — What the Validator Blocks

| SQL keyword | Why blocked |
|---|---|
| `DROP` | Would delete entire tables |
| `DELETE` | Would remove rows |
| `INSERT` | Would add fake data |
| `UPDATE` | Would modify existing data |
| `ALTER` | Would change table structure |
| `TRUNCATE` | Would wipe all data |

Only `SELECT` queries are allowed. If the LLM generates anything else, the pipeline stops immediately and returns an error message without touching the database.

---

## Groq Model Used

| Setting | Value |
|---|---|
| Provider | Groq |
| Model | `llama-3.3-70b-versatile` |
| Temperature (SQL) | 0 — deterministic, same question = same SQL |
| Temperature (summary) | 0.3 — slight variation for natural language |
| API key env var | `GROQ_API_KEY` |

---

## Real Output Example

```
Question: How many customers are from each country?
------------------------------------------------------------
Generated SQL:
SELECT country, COUNT(*) as total FROM customers
GROUP BY country ORDER BY total DESC LIMIT 100

Query returned 20 rows

Answer:
The database contains customers from 20 different countries.
The United States has the most customers with 1,245, followed by
the United Kingdom with 832 and Canada with 654...
```

---

