import os
from groq import Groq
from src.utils.schema_loader import get_schema

try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except:
    client = None

MODEL  = "llama-3.3-70b-versatile"

def generate_sql(user_question):
    try:
        schema = get_schema()
    except:
        schema = ""

    try:
        prompt = f"""You are an expert SQL assistant. Given the database schema below, 
write a valid SQLite SQL query to answer the user's question.
ONLY generate SQL if the question is related to the database contents.
If the question is completely unrelated to the database, return exactly: NOT_RELEVANT

RULES:
- Return ONLY the SQL query, nothing else
- No explanations, no markdown, no backticks
- Always use COUNT(*) never COUNT index or COUNT field
- Use proper SQL syntax — all functions must have parentheses
- Use only tables and columns that exist in the schema
- Always use LIMIT 100 to avoid huge results

DATABASE SCHEMA:
{schema}

USER QUESTION:
{user_question}

SQL QUERY:"""
    except:
        return ""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        sql = response.choices[0].message.content.strip()
    except:
        return ""

    try:
        sql = sql.replace("```sql", "").replace("```", "").strip()
    except:
        pass

    return sql


if __name__ == "__main__":
    try:
        question = "Show me the top 5 customers by age"
        sql      = generate_sql(question)
        print(f"Question: {question}")
        print(f"Generated SQL:\n{sql}")
    except:
        pass