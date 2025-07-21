from flask import Flask, render_template_string, request
from ragbot import answer_question

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <title>RAGbot Web UI</title>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap' rel='stylesheet'>
  <link rel="icon" href="https://img.icons8.com/fluency/48/robot-2.png">
  <style>
    body {
      background: linear-gradient(120deg, #d1fae5 0%, #bbf7d0 100%);
      font-family: 'Inter', sans-serif;
      min-height: 100vh;
      margin: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.4s;
    }
    .container {
      background: rgba(255, 255, 255, 0.92);
      border-radius: 32px;
      box-shadow: 0 8px 40px 0 rgba(16, 185, 129, 0.18);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      padding: 3.5rem 3rem 2.8rem 3rem;
      max-width: 600px;
      width: 100%;
      margin: 2rem;
      border: 2px solid #6ee7b7;
      position: relative;
      animation: fadeIn 0.7s;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(30px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .logo {
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 1.6rem;
    }
    .logo img {
      width: 54px;
      height: 54px;
      margin-right: 1rem;
    }
    .logo span {
      font-size: 2.5rem;
      font-weight: 700;
      color: #10b981;
      letter-spacing: -1px;
    }
    h1 {
      display: none;
    }
    form {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 100%;
    }
    label {
      font-weight: 700;
      color: #065f46;
      margin-bottom: 1.1rem;
      display: block;
      font-size: 1.45rem;
      text-align: center;
    }
    input[type="text"] {
      width: 90%;
      padding: 1.3rem 1.3rem;
      border: 2.5px solid #6ee7b7;
      border-radius: 18px;
      font-size: 1.35rem;
      margin-bottom: 2.1rem;
      outline: none;
      background: #f0fdf4;
      color: #222;
      box-shadow: 0 2px 12px rgba(16,185,129,0.07);
      transition: box-shadow 0.2s, background 0.2s, border 0.2s;
      text-align: center;
    }
    input[type="text"]:focus {
      background: #fff;
      box-shadow: 0 0 0 3px #34d399;
      border: 2.5px solid #34d399;
    }
    input[type="submit"] {
      background: linear-gradient(90deg, #34d399 0%, #10b981 100%);
      color: #fff;
      border: none;
      border-radius: 18px;
      padding: 1.1rem 4.5rem;
      font-size: 1.35rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 2px 16px rgba(16,185,129,0.13);
      transition: background 0.2s, transform 0.1s, box-shadow 0.2s;
      letter-spacing: 0.5px;
      display: block;
      margin: 0 auto;
    }
    input[type="submit"]:hover {
      background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
      transform: translateY(-2px) scale(1.04);
      box-shadow: 0 4px 24px rgba(16,185,129,0.18);
    }
    input:focus, button:focus {
      outline: none;
      box-shadow: 0 0 0 2px #10b981;
    }
    .answer-box {
      margin-top: 2.7rem;
      background: rgba(236, 253, 245, 0.98);
      border-left: 8px solid #10b981;
      border-radius: 16px;
      padding: 1.7rem 1.3rem;
      font-size: 1.25rem;
      color: #064e3b;
      box-shadow: 0 2px 18px rgba(16,185,129,0.11);
      word-break: break-word;
      animation: answerPop 0.5s;
    }
    @keyframes answerPop {
      from { opacity: 0; transform: scale(0.97); }
      to { opacity: 1; transform: scale(1); }
    }
    ::placeholder {
      color: #6ee7b7;
      opacity: 1;
      font-size: 1.25rem;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="logo">
      <img src="https://img.icons8.com/fluency/48/robot-2.png" alt="RAGbot logo">
      <span>RAGbot</span>
    </div>
    <form method="post" autocomplete="off">
      <label for="question">Ask me anything:</label>
      <input type="text" id="question" name="question" placeholder="Type your question here..." required autofocus>
      <input type="submit" value="Ask">
    </form>
    {% if answer is not none %}
      <div class="answer-box">
        <strong>Answer:</strong><br>
        {{ answer }}
      </div>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    if request.method == "POST":
        question = request.form.get("question", "")
        if question:
            answer = answer_question(question)
    return render_template_string(HTML, answer=answer)

if __name__ == "__main__":
    app.run(debug=True) 