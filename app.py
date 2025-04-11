from flask import Flask, render_template, request, redirect, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "secret"  # セッション用（本番では強いキーを）

# クイズをDBから取得
def get_all_questions():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz")
    rows = cursor.fetchall()
    conn.close()
    questions = []
    for row in rows:
        qid, question, answer, opt1, opt2, opt3, description = row
        options = [answer, opt1, opt2, opt3]
        random.shuffle(options)
        questions.append({
            "id": qid,
            "question": question,
            "answer": answer,
            "options": options,
            "description": description
        })
    return questions

@app.route("/", methods=["GET", "POST"])
def quiz():
    # 🔁 アプリ再起動時に状態リセット
    if "questions" not in session:
        session.clear()
        all_questions = get_all_questions()
        session["questions"] = random.sample(all_questions, 3)
        session["current"] = 0
        session["score"] = 0
        session["show_description"] = False

    questions = session["questions"]
    current = session["current"]
    show_description = session.get("show_description", False)

    if request.method == "POST" and current < len(questions):
        selected = request.form["choice"]
        correct = questions[current]["answer"]
        description = questions[current]["description"]
        result = "正解！" if selected == correct else f"不正解！正解は「{correct}」"
        if selected == correct:
            session["score"] += 1
        session["last_result"] = result
        session["last_description"] = description
        session["show_description"] = True
        return redirect("/")

    if show_description:
        return render_template("description.html",
                               result=session["last_result"],
                               description=session["last_description"],
                               current=session["current"] + 1,
                               total=len(questions))

    if current >= len(questions):
        if request.method == "POST":
            name = request.form["name"]
            score = session["score"]
            conn = sqlite3.connect('quiz.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user (name, score) VALUES (?, ?)", (name, score))
            conn.commit()
            cursor.execute("SELECT name, score FROM user ORDER BY score DESC, id ASC")
            rankings = cursor.fetchall()
            conn.close()
            session.clear()
            return render_template("result.html", name=name, score=score, total=len(questions), rankings=rankings)

        return render_template("name_input.html", total=len(questions), score=session["score"])

    question_data = questions[current]
    return render_template("quiz.html", question=question_data["question"],
                           options=question_data["options"],
                           correct=question_data["answer"])

@app.route("/next")
def next_question():
    session["current"] += 1
    session["show_description"] = False
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
