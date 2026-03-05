from flask import Flask, render_template
from google import genai
from google.genai import types
app = Flask(__name__)

client = genai.Client(api_key = "AIzaSyB36C1zyAp97-SL0RRtbvWJLWeW1rWffR8")


@app.route("/")
def index():
    # 'index.html' refers to the file inside the /templates folder
    return render_template("index.html", result="Flask is working!")

if __name__ == "__main__":
    app.run(debug=True)
