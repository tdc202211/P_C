import json
import sqlite3

# JSONファイルを読み込む
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# DB接続
conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# データ挿入
for item in data:
    cursor.execute('''
        INSERT INTO quiz (question, answer, option1, option2, option3, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        item['question'],
        item['answer'],
        item['option1'],
        item['option2'],
        item['option3'],
        item['description']
    ))

conn.commit()
conn.close()

print("✅ JSONから問題をDBに保存しました。")
