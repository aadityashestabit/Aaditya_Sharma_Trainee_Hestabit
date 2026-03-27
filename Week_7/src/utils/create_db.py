# run this as a one-time setup script: src/utils/create_db.py
import pandas as pd
import sqlite3
import os

os.makedirs("src/data/sql", exist_ok=True)

# load your CSV
df = pd.read_csv("src/data/raw/people-10000.csv")

# clean column names — remove spaces and special chars
df.columns = [c.strip().replace(" ", "_").replace("-", "_").lower() for c in df.columns]

# save to SQLite
conn = sqlite3.connect("src/data/sql/enterprise.db")
df.to_sql("customers", conn, if_exists="replace", index=False)
conn.close()

print("Database created at src/data/sql/enterprise.db")
print(f"Table: customers — {len(df)} rows, columns: {list(df.columns)}")