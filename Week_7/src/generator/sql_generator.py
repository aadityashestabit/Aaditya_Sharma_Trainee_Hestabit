import os
from groq import Groq
from src.utils.schema_loader import get_schema

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL  = "llama-3.3-70b-versatile"

def generate_sql(user_question):
    schema = get_schema()

    prompt = f"""You are an expert SQL assistant. Given the database schema below, 
write a valid SQLite SQL query to answer the user's question.

RULES:
- Return ONLY the SQL query, nothing else
- No explanations, no markdown, no backticks
- Use only tables and columns that exist in the schema
- Always use LIMIT 100 to avoid huge results

DATABASE SCHEMA:
{schema}

USER QUESTION:
{user_question}

SQL QUERY:"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    # clean up in case LLM adds backticks anyway
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql


if __name__ == "__main__":
    question = "Show me the top 5 customers by age"
    sql      = generate_sql(question)
    print(f"Question: {question}")
    print(f"Generated SQL:\n{sql}")