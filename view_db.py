import sqlite3

conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM quiz")
rows = cursor.fetchall()

for row in rows:
    print(f"ID: {row[0]}")
    print(f"問題: {row[1]}")
    print(f"正解: {row[2]}")
    print(f"選択肢1: {row[3]}")
    print(f"選択肢2: {row[4]}")
    print(f"選択肢3: {row[5]}")
    print(f"解説: {row[6]}")
    print("-" * 40)

conn.close()
