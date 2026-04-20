import sqlite3
import re
from collections import deque


class SessionMemory:
    def __init__(self, db_path: str = "memory/long_term.db", max_turns: int = 10):
        self.db_path = db_path
        self.recent_turns = deque(maxlen=max_turns)  # short-term sliding window
        self._init_db()

    def _init_db(self):
        # create the facts table if it doesn't exist yet
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    fact      TEXT NOT NULL,
                    source    TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    # short-term memory 
    def add_turn(self, role: str, content: str):
        self.recent_turns.append({"role": role, "content": content})

    def format_recent_context(self) -> str:
        if not self.recent_turns:
            return "No recent conversation yet."
        lines = []
        for turn in self.recent_turns:
            label = "User" if turn["role"] == "user" else "Assistant"
            lines.append(f"{label}: {turn['content']}")
        return "\n".join(lines)

    # long-term memory (SQLite) 

    def store_facts(self, facts: list, source: str = "conversation"):
        if not facts:
            return
        with sqlite3.connect(self.db_path) as conn:
            for fact in facts:
                fact = fact.strip()
                if fact:
                    conn.execute(
                        "INSERT INTO facts (fact, source) VALUES (?, ?)",
                        (fact, source)
                    )
            conn.commit()

    def search_facts(self, query: str, limit: int = 5) -> list:
        # simple keyword search — splits query into words and looks for any match
        words = [w.lower() for w in query.split() if len(w) > 3]
        if not words:
            return []
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            placeholders = " OR ".join(["LOWER(fact) LIKE ?" for _ in words])
            params = [f"%{w}%" for w in words]
            rows = conn.execute(
                f"SELECT fact FROM facts WHERE {placeholders} ORDER BY timestamp DESC LIMIT ?",
                params + [limit]
            ).fetchall()
        return [row["fact"] for row in rows]

    def format_fact_results(self, facts: list) -> str:
        if not facts:
            return "No relevant facts found."
        return "\n".join(f"- {f}" for f in facts)

    def extract_important_facts(self, text: str) -> list:
        # pull out sentences that look like they contain useful persistent info
        # looks for patterns like "my name is", "I am", "I work at" etc.
        important_patterns = [
            r"my name is .+",
            r"i am .+",
            r"i work .+",
            r"i live .+",
            r"i like .+",
            r"i prefer .+",
            r"i have .+",
            r"i use .+",
            r"remember that .+",
            r"don't forget .+",
        ]
        facts = []
        text_lower = text.lower()
        for pattern in important_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                # capitalise and clean up
                fact = match.strip().capitalize()
                if len(fact) > 10:  # skip very short matches
                    facts.append(fact)
        return facts

    def clear_session(self):
        self.recent_turns.clear()