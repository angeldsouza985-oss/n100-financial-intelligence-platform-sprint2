import sqlite3

conn = sqlite3.connect("nifty100.db")
cur = conn.cursor()

print("=== TABLES ===")
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
for row in cur.fetchall():
    print(row)

print("\n=== COMPANIES COLUMNS ===")
cur.execute("PRAGMA table_info(companies);")
for row in cur.fetchall():
    print(row)

conn.close()