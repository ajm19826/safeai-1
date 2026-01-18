import sqlite3

class MemoryGraph:
    def __init__(self, db_path="memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        # use 'props' instead of 'values'
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                name TEXT PRIMARY KEY,
                props TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS links (
                concept TEXT,
                related TEXT
            )
        """)
        self.conn.commit()

    def add_concept(self, name, value=None):
        name = name.lower()
        if value:
            value = value.lower()
            existing = self.cursor.execute(
                "SELECT props FROM concepts WHERE name = ?", (name,)
            ).fetchone()
            if existing:
                values = set(existing[0].split(","))
                values.add(value)
                self.cursor.execute(
                    "UPDATE concepts SET props=? WHERE name=?",
                    (",".join(values), name)
                )
            else:
                self.cursor.execute(
                    "INSERT INTO concepts (name, props) VALUES (?, ?)",
                    (name, value)
                )
            self.conn.commit()

    def link(self, a, b):
        a, b = a.lower(), b.lower()
        self.cursor.execute("INSERT INTO links (concept, related) VALUES (?, ?)", (a, b))
        self.cursor.execute("INSERT INTO links (concept, related) VALUES (?, ?)", (b, a))
        self.conn.commit()

    def knows(self, concept):
        return self.cursor.execute(
            "SELECT 1 FROM concepts WHERE name=?", (concept.lower(),)
        ).fetchone() is not None

    def get_properties(self, concept):
        row = self.cursor.execute(
            "SELECT props FROM concepts WHERE name=?", (concept.lower(),)
        ).fetchone()
        return row[0].split(",") if row else []

    def related(self, concept):
        rows = self.cursor.execute(
            "SELECT related FROM links WHERE concept=?", (concept.lower(),)
        ).fetchall()
        return [r[0] for r in rows]
