from flask import Flask, render_template, request
import sqlite3
import random

app = Flask(__name__)

def get_random_question():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        qid, question, correct, *others = row
        options = others + [correct]
        random.shuffle(options)
        return {'id': qid, 'question': question, 'options': options, 'correct': correct}
    return None

@app.route("/", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        selected = request.form["choice"]
        correct = request.form["correct"]
        result = "正解！" if selected == correct else f"不正解！正解は「{correct}」"
        return render_template("quiz.html", result=result, **get_random_question())

    return render_template("quiz.html", result=None, **get_random_question())

if __name__ == "__main__":
    app.run(debug=True)
