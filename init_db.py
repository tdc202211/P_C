import sqlite3

conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# 新しいテーブル定義（descriptionを追加）
cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    description TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("✅ 新しいquizテーブルを作成しました。")
