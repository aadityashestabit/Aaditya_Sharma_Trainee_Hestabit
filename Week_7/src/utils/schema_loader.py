import sqlite3

DB_PATH = "src/data/sql/enterprise.db"

def get_schema():
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    schema_text = ""
    for table in tables:
        # get column info for each table
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()

        # get a sample row so LLM understands the data
        cursor.execute(f"SELECT * FROM {table} LIMIT 3")
        sample_rows = cursor.fetchall()

        schema_text += f"Table: {table}\n"
        schema_text += "Columns:\n"
        for col in columns:
            schema_text += f"  - {col[1]} ({col[2]})\n"
        schema_text += "Sample rows:\n"
        for row in sample_rows:
            schema_text += f"  {row}\n"
        schema_text += "\n"

    conn.close()
    return schema_text

def get_table_names():
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

if __name__ == "__main__":
    print(get_schema())