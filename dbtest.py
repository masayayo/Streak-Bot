import sqlite3
from datetime import datetime

conn = sqlite3.connect('streakbot.db')
c = conn.cursor()

c.execute("update USERS set CURRENT = (HIGHEST + CURRENT) WHERE DAILY = 0")
for rows in c.execute("SELECT CURRENT, ID FROM USERS"):
    print(rows)
conn.close()

# i = datetime.now()
# print(f"Time until execute: {24 - i.hour - i.minute/60}")
