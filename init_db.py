import sqlite3

# quiz.db に接続（ファイルがなければ自動で作成される）
conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# テーブルを作成（なければ）
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL
)
''')

# テスト用の1問を追加（既に入っているかチェックしてから）
cursor.execute("SELECT COUNT(*) FROM questions")
if cursor.fetchone()[0] == 0:
    cursor.execute('''
    INSERT INTO questions (question, correct_answer, option1, option2, option3)
    VALUES (?, ?, ?, ?, ?)
    ''', ("「漢」の読みは？", "かん", "こう", "けん", "かい"))

# 保存して閉じる
conn.commit()
conn.close()

print("✅ quiz.db にテーブルとテスト問題を作成しました。")
