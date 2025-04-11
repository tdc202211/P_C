from flask import Flask, render_template, request, redirect, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "secret"  # セッション用キー（本番では安全な値に）

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
    if "questions" not in session:
        # 初回アクセス：ランダムに3問抽出してセッションへ
        all_questions = get_all_questions()
        session["questions"] = random.sample(all_questions, 3)
        session["current"] = 0
        session["score"] = 0
        session["show_description"] = False

    questions = session["questions"]
    current = session["current"]
    show_description = session.get("show_description", False)

    if request.method == "POST":
        selected = request.form["choice"]
        correct = questions[current]["answer"]
        description = questions[current]["description"]
        result = "正解！" if selected == correct else f"不正解！正解は「{correct}」"
        if selected == correct:
            session["score"] += 1

        session["last_result"] = result
        session["last_description"] = description
        session["show_description"] = True
        return redirect("/")  # 解説表示へリダイレクト

    if show_description:
        # 解説画面
        return render_template("description.html",
                               result=session["last_result"],
                               description=session["last_description"],
                               current=session["current"] + 1,
                               total=len(questions))

    if current >= len(questions):
        score = session["score"]
        session.clear()
        return render_template("result.html", score=score, total=len(questions))

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
