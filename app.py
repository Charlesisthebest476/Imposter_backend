from flask import Flask, render_template
from google import genai
from google.genai import types
import os
app = Flask(__name__)

client = genai.Client(api_key = "AIzaSyB36C1zyAp97-SL0RRtbvWJLWeW1rWffR8")


@app.route("/")
def index():
    # 'index.html' refers to the file inside the /templates folder
    return render_template("index.html", result="Flask is working!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) #5000 is backup
    app.run(host='0.0.0.0', port=port, debug=True) #make flask available to the world and set debug to true for development
    app.run(debug=True)
