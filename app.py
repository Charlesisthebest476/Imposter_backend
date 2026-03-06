"""Version 1.0: basic skeleton"""


from flask import Flask, render_template, request
from google import genai
from google.genai import types
import os
app = Flask(__name__)


client = genai.Client(api_key = "AIzaSyB36C1zyAp97-SL0RRtbvWJLWeW1rWffR8")
prompt = ["INSERT categories here"]

total_tokens = client.model.count_tokens(
    model = "gemini-3.1-flash-lite-preview",
    contents = prompt,
)

def gemini():
    response = client.models.generate_content(
        model = "gemini-3.1-flash-lite-preview",
        contents = prompt,
    )

    return response



@app.route("/", methods=['GET', 'POST'])
def index():
    categories = ["Category 1", "Category 2", "Category 3"]  # Example categories
    result = None

    if request.method == 'POST':
    # Get the data from the form
        num_of_players = request.form['num_of_players']
        num_of_imposters = request.form['num_of_imposters']
        category = request.form['category']
        result = 'results received'
    return render_template("index.html", categories=categories, result=result)





if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True) #make flask available to the world and set debug to true for development
