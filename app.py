from flask import Flask, render_template
from google import genai
from google.genai import types
app = Flask(__name__)

client = genai.Client(api_key = GEMINI_API_KEY)


@app.route("/")
def index():
    # 'index.html' refers to the file inside the /templates folder
    return render_template("index.html", title="Flask is working!")

if __name__ == "__main__":
    app.run(debug=True)
