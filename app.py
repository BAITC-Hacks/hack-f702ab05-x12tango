from flask import Flask, jsonify, render_template, request

from faq_engine import find_answer, load_faq

app = Flask(__name__)
faq = load_faq()


@app.route("/")
def index():
    questions = [question for question, _ in faq]
    return render_template("index.html", questions=questions)


@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()

    if not question:
        return jsonify({"error": "empty question"}), 400

    answer = find_answer(question, faq)
    return jsonify({"answer": answer or "не знаю", "matched": answer is not None})


if __name__ == "__main__":
    app.run(debug=True)
