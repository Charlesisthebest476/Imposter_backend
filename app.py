"""
Imposter
March 6th - Version 1.0: basic skeleton
March 7th - Version 1.1: added game logic for game.html
March 12th - Version 1.2: environment key set
March 23rd - Version 1.3: Successful connection with AI
March 25th - Version 1.4: Debugging the issue with the Gemini server not responding
March 30th - Version 1.5: Added environment variables to ensure security
April 1st - Version 1.6: Replaced URL data passing with Flask sessions for better security
April 8th - Version 1.7: Working on voting system
April 9th - Version 1.8: Completing the prototype, including final game logic, voting system, and imposter guess word
April 14th - Version 1.9: Beta testing
April 29th - Version 1.9.1: Attempting to fix AI iteration issue using class
May 25th - Version 1.9.2: Adding a different mode, fixed different imposter words, revised the prompt
"""


from flask import Flask, render_template, request, redirect, url_for
from google import genai
from google.genai import types
import os
import random
from flask import session
from rules import Rules #import rules class



rules = Rules()



CATEGORIES = ["Food", "Animal", "Location", "Hobbies", "Household", "Movies/TV", "Occupations", "Sports"]  # Example categories
AI_MODELS = ["gemini-3.1-flash-lite", "gemini-2.5-flash-lite", "gemini-2.0-flash-lite", "gemini-2.5-flash"]
KEY = os.environ.get("KEY")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


client = genai.Client(api_key=KEY) #replace with actual API


# Check token usage(not used currently)
"""
total_tokens = client.models.count_tokens(
    model = "gemini-3.1-flash-lite-preview",
    contents =
)
"""


class Model:
    content = ("Select one category from the list below. Generate a random target word (concept, object, or place; max 3 words) belonging to that category. "
    "The target word must be a specific, concrete item, object, or concept within that category, NOT a broad category name itself."
    "The criteria for word generation are to avoid complex vocabulary and to focus on words that are common. This means that a native sixth grader should be "
    "able to understand the words provided. Provide 5 hint words that are related but not synonyms and do not contain the target word. Hints should avoid "
    "immediately obvious associations. The hint word should not be a subcategory of the target word. A player "
    "should NOT be able to easily guess the target word just from the hints, but once the target word is revealed, the connection to the hints must feel "
    "logical in reverse. Output Format: A single comma-separated string containing the target word followed by the five hints. The category given is "
    )

    safety_settings=[
        types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="BLOCK_ONLY_HIGH",  # Block few
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="BLOCK_ONLY_HIGH",  # Block few
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="BLOCK_ONLY_HIGH",  # Block few
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="BLOCK_ONLY_HIGH",  # Block few
        ),
        ]
    

    def __init__(self, model, cat):
        self.model = model
        self.cat = cat
    
    def select_thinking_build(self):
        if "3.1" in self.model:
            return types.ThinkingConfig(thinking_level = "MEDIUM")
        elif "2.5" in self.model:
            return types.ThinkingConfig(thinking_budget= 3000)
        return None

    def get_response(self):
        try:
            config = self.select_thinking_build()
            cont = self.__class__.content + self.cat + f". The hint words cannot be one of the following words: {',' .join(session.get('previous_words', []))}"

            response = client.models.generate_content(
                model = self.model,
                config = types.GenerateContentConfig(
                    thinking_config = config,
                    safety_settings=self.__class__.safety_settings
                ),
                contents = cont
            )
            return response.text
        except Exception as e:
            print(f"Model {self.model} failed to generate a response. {e}")#debug
            return None

def gemini(cat):
    response = None
    i = 0
    while not response and i < len(AI_MODELS):
        model = Model(AI_MODELS[i], cat)
        response = model.get_response()
        print(response)
        i+=1
    if not response:
        raise Exception("All AI models failed to generate a response") #if all models fail, raise an exception to be caught in the index function
    return response.split(",")

"""old code
#Call function to prompt gemini
def gemini(cat):
    i = 0
    response = None
    while i < len(AI_MODELS) and response is None: #try different models if the first one fails
        if i == 0: #gemini-3.1-flash-lite-preview
            try:
                response = client.models.generate_content(
                    model = AI_MODELS[i],
                    config = types.GenerateContentConfig(
                        thinking_config = types.ThinkingConfig(thinking_level = "MEDIUM"),
                        safety_settings=[
                            types.SafetySetting(
                                category="HARM_CATEGORY_HARASSMENT",
                                threshold="BLOCK_ONLY_HIGH",  # Block few
                            ),
                            types.SafetySetting(
                                category="HARM_CATEGORY_HATE_SPEECH",
                                threshold="BLOCK_ONLY_HIGH",  # Block few
                            ),
                            types.SafetySetting(
                                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                threshold="BLOCK_ONLY_HIGH",  # Block few
                            ),
                            types.SafetySetting(
                                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                                threshold="BLOCK_ONLY_HIGH",  # Block few
                            ),
                        ]
                    ),
                    contents = ("Given the following categories provided, randomly select one of the categories, then generate a random word that relates to one of them."
                        "Based off of that generated word, generate a list of 5 hint words that relate to the word. Make sure that the hint words do not contain the original word in itself,"
                        "or is a direct synonym of it. The hint words should not be too obvious such that the first instinctual connection is to the original word."
                    "The original word does not necessarily have to be one singular word, but must be a single object, or concept, or place. The generated words must not exceed a length of 3 words. "
                    "The hint words must be 1 word in length. "
                    f"Respond with only the generated words in a string, no other words, with each separated with a comma. The categories are {', '.join(cat)}"
                    )#sectioned into different lines for readability, the local var cat is sent to the AI for word generation
                )
                #print(response.text) #debug
            except:
                response = None
        elif i == 1: #gemini-2.5-flash-lite
            try:
                response = client.models.generate_content(
                    model = AI_MODELS[i],
                    config = types.GenerateContentConfig(
                        thinking_config = types.ThinkingConfig(thinking_budget = 3000),
                        safety_settings=[
                            types.SafetySetting(
                                category="HARM_CATEGORY_HARASSMENT",
                                threshold="BLOCK_ONLY_HIGH",  # Block few
                            ),
                            types.SafetySetting(
                                category="HARM_CATEGORY_HATE_SPEECH",
                                threshold="BLOCK_ONLY_HIGH",  # Block few
                            ),
                            types.SafetySetting(
                                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                threshold="BLOCK_ONLY_HIGH",  # Block few
                            ),
                            types.SafetySetting(
                                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                                threshold="BLOCK_ONLY_HIGH",  # Block few
                            ),
                        ]
                    ),
                    contents = ("Given the following categories provided, randomly select one of the categories, then generate a random word that relates to one of them."
                        "Based on that generated word, generate a list of 5 hint words that relate to the word. Make sure that the hint words do not contain the original word in itself,"
                        "or is a direct synonym of it. The hint words should not be too obvious such that the first instinctual connection is to the original word."
                    "The original word does not necessarily have to be one singular word, but must be a single object, or concept, or place. The generated words must not exceed a length of 3 words. "
                    "The hint words must be 1 word in length. "
                    f"Respond with only the generated words in a string, no other words, with each separated with a comma. The categories are {', '.join(cat)}"
                    )#sectioned into different lines for readability, the local var cat is sent to the AI for word generation
                )
                #print(response.text) #debug
            except:
                response = None
        else: #gemini-2.0-flash-lite
            try:
                response = client.models.generate_content(
                    model = AI_MODELS[i],
                    config = types.GenerateContentConfig(
                        safety_settings=[
                            types.SafetySetting(
                                category="HARM_CATEGORY_HARASSMENT",
                                threshold="BLOCK_ONLY_HIGH",  # Block few
                            ),
                            types.SafetySetting(
                                category="HARM_CATEGORY_HATE_SPEECH",
                                threshold="BLOCK_ONLY_HIGH",  # Block few
                            ),
                            types.SafetySetting(
                                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                threshold="BLOCK_ONLY_HIGH",  # Block few
                            ),
                            types.SafetySetting(
                                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                                threshold="BLOCK_ONLY_HIGH",  # Block few
                            ),
                        ]
                    ),
                    contents = ("Given the following categories provided, randomly select one of the categories, then generate a random word that relates to one of them."
                        "Based off of that generated word, generate a list of 5 hint words that relate to the word. Make sure that the hint words do not contain the original word in itself,"
                        "or is a direct synonym of it. The hint words should not be too obvious such that the first instinctual connection is to the original word."
                    "The original word does not necessarily have to be one singular word, but must be a single object, or concept, or place. The generated words must not exceed a length of 3 words. "
                    "The hint words must be 1 word in length. "
                    f"Respond with only the generated words in a string, no other words, with each separated with a comma. The categories are {', '.join(cat)}"
                    )#sectioned into different lines for readability, the local var cat is sent to the AI for word generation
                )
                #print(response.text) #debug
            except:
                response = None
        i +=1
    if response is None:
        raise Exception("All AI models failed to generate a response") #if all models fail, raise an exception to be caught in the index function
    #returns a list and first word is the normal word and second word is the imposter word
    return response.text.split(",") #split the response into two words based on the comma
"""




def chooseimposter(num_of_players, num_of_imposters):
    # Create a list of players
    players = list(range(1, num_of_players + 1))

    # Randomly select imposters
    imposters = random.sample(players, num_of_imposters)

    return imposters

def pick_random_word(wordList, number_of_players):
    selected_words = []
    for _ in range(number_of_players):
        selected_words.append(random.choice(wordList))
    return selected_words




@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        mode = request.form.get('mode')
        return redirect(url_for('start', mode=mode))
    return render_template("index.html")





@app.route("/start", methods=['GET', 'POST'])
def start():
    categories = CATEGORIES
    mode = request.args.get('mode')


    if request.method == 'POST':
        # Get the data from the form
        num_of_players = int(request.form['num_of_players'])
        num_of_imposters = request.form.get('num_of_imposters')
        if num_of_imposters:
            num_of_imposters = int(num_of_imposters)
        else:
            num_of_imposters = random.randint(1, num_of_players - 1)
        
        if num_of_imposters > num_of_players:
            return redirect(url_for('error')) # Redirect to an error page if the number of imposters is greater than the number of players
        imposters = chooseimposter(num_of_players, num_of_imposters)
        player_category_selection = request.form.getlist('category')
        #print(f"Player category selection: {player_category_selection}") #debug


        try: #code in case gemini fails to generate words
            word = gemini(random.choice(player_category_selection))
            setup_data = {
                "num_of_players": num_of_players,
                "num_of_imposters": num_of_imposters,
                "category": player_category_selection,
                "imposters": imposters,
                "normal_word": word[0], 
                "imposter_word":pick_random_word(word[1:], num_of_imposters), 
                "current_player": 1,
                "current_role": "hidden",
                "mode": mode
            }
            session['game_data'] = setup_data  # Store data in session
            return redirect(url_for('player_names'))
        except Exception as e:
            session['error'] = str(e)
            return redirect(url_for('error')) # Redirect to an error page if gemini fails to generate words
    return render_template("start.html", categories=categories, mode=mode)




@app.route("/player_names", methods=['GET', 'POST'])
def player_names():
    if request.method == 'POST':
        name_list = []
        for value in request.form.items():
            name_list.append(value[1]) #this is the content
        session['game_data']['player_names'] = name_list
        session['game_data']['imposter_counter'] = 0
        session.modified = True
        return redirect(url_for('game'))
    return render_template("player_names.html", game_info=session.get('game_data')) #pass the info from the index page to the player names page so we can use it in the form

#now the dictionary looks like this:
"""
{
    "num_of_players": 5,
    "num_of_imposters": 2,
    "category": ["Food"],
    "imposters": [2, 4],
    "normal_word": "Pizza",
    "imposter_word": ["Burger", "pineapple"],
    "current_player": 1,
    "current_role": "hidden",
    "player_names": ["Alice", "Bob", "Charlie", "David", "Eve"]
}
"""



@app.route("/game", methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        action = request.form['action']




        #for changing variables in the dictionary
        if action == "Next Player":
            #reset role and word for next player
            session['game_data']['current_role'] = "hidden"
            session['game_data']['word'] = ''
            session['game_data']['current_player'] += 1
        elif action == "Click Me to Reveal Role":
            #detect imposter
            if session['game_data']['current_player'] in session['game_data']['imposters']:
                session['game_data']['current_role'] = "Imposter"
                session['game_data']['word'] = session['game_data']["imposter_word"][session['game_data']['imposter_counter']]
                session['game_data']['imposter_counter'] += 1
            else:
                session['game_data']['current_role'] = "Citizen"
                session['game_data']['word'] = session['game_data']['normal_word']
        session.modified = True #mark the session as modified to ensure changes are saved
        if action == "See Who'll Start":
            return redirect(url_for('who_start'))
    return render_template("game.html", game_info=session.get('game_data'))


@app.route("/who_start", methods=['POST', 'GET'])
def who_start():
    if request.method == 'POST':
        return redirect(url_for('voting'))
    session['game_data']['starting_player'] = random.randint(0, session['game_data']['num_of_players'] - 1) #randomly select a player to start, this is completely random so no hint is given to the players who are trying to find the imposter
    session.modified = True
    return render_template("who_start.html", game_info=session.get('game_data')) 

#now the dictionary looks like this:
"""
{
    "num_of_players": 5,
    "num_of_imposters": 2,
    "category": ["Food"],
    "imposters": [2, 4],
    "normal_word": "Pizza",
    "imposter_word": ["Burger", "pineapple"],
    "current_player": 1,
    "current_role": "hidden",
    "player_names": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "starting_player": 3, 
    "error": "All AI models failed to generate a response"
}
"""


@app.route("/voting", methods=['POST', 'GET'])
def voting():
    game_data = session['game_data']

    if request.method == 'POST':
        action = request.form['action']
        #voting logic
        voted_player = request.form['voted_player']
        #add player vote to the voting result, if the player is already voted for, add 1, if not, set it to 1
        game_data['voting_result'][voted_player] = game_data['voting_result'][voted_player] + 1 if game_data['voting_result'].get(voted_player, None) is not None else 1
        
        print(f"voting_result: {game_data['voting_result']}") #debug

        game_data['current_player'] += 1
        if action == "See Voting Result":
            session.modified = True
            return redirect(url_for('vote_result'))
    else:
        game_data['voting_result'] = {}
        game_data['current_player'] = 1

    #for frontend display of which players can be voted for
    vote_list = []
    for player in game_data['player_names']:
        if player != game_data['player_names'][game_data['current_player'] - 1]: #-1 cause player numbers start with 1 and index starts with 0
            vote_list.append(player)
    game_data['current_vote_list'] = vote_list

    session.modified = True
    return render_template("voting.html", game_info=session.get('game_data')) 

#visualization of the current session dictionary
"""
{
    "num_of_players": 5,
    "num_of_imposters": 2,
    "category": ["Food"],
    "imposters": [2, 4],
    "normal_word": "Pizza",
    "imposter_word": "Burger",
    "current_player": 1,
    "current_role": "hidden",
    "player_names": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "starting_player": 3,
    "error": "All AI models failed to generate a response",
    "current_vote_list": ["Alice", "Bob", "Charlie", "David"],
    "voting_result": {"Alice": 3, "Bob": 1, "David": 1},
}
"""

@app.route("/vote_result", methods=['POST', 'GET'])
def vote_result():
    game_data = session['game_data']
    if request.method == 'POST':
        action = request.form['action']
        if action == "Continue":
            #game logic for determining whether to ask the imposter for the word or end the game based on the voting result
            imposter_names = [game_data['player_names'][player-1] for player in game_data['imposters']] #-1 because imposter is starts from 1
            game_data['imposter_names'] = imposter_names 
            session.modified = True
            if game_data['most_voted_player'] in imposter_names:
                return redirect(url_for('imposter_guess'))
            else:
                return redirect(url_for('game_result'))
        elif action == "Revote":
            #need to revote
            return redirect(url_for('voting'))
    # Show an ordered list, from top to bottom of the players with most to least votes
    # I think there are two ways to approach this:
    # 1. convert dictionary to 2-d list, then sort that 2-d list based on the second element. 
    #    With my current knowledge of python, this will take a while as I have to write a
    #    sorting alg for 2-d list and run it
    # 2. clone the dictionary, then repeatedly find the max value in the dictionary, 
    #    add that key to the ordered list, then remove that key from the dictionary, 
    #    and repeat until the dictionary is empty(essentially selection sort). 
    #    This will be faster to implement as I can use the built in max function for dictionaries, 
    #    but it is less efficient as it has to loop through the dictionary multiple times.
    # However, given that the number of players is at most 10, this inefficiency is negligible and 
    # I will go with this approach for simplicity and speed of implementation.
    residuals_player = game_data['voting_result'].copy()
    ordered_players = []
    while len(residuals_player) > 0:
        max_voted_player = max(residuals_player, key=residuals_player.get)#find the key with the max value
        ordered_players.append(max_voted_player)
        del residuals_player[max_voted_player]
    game_data['ordered_players'] = ordered_players
    
    if game_data['voting_result'][ordered_players[0]] == game_data['voting_result'][ordered_players[1]]:
        game_data['most_voted_player'] = None
    else:
        #decision for asking the imposter for word or not
        game_data['most_voted_player'] = ordered_players[0]


    session.modified = True
    return render_template("vote_result.html", game_info=session.get('game_data'))

@app.route("/imposter_guess", methods=['POST', 'GET'])
def imposter_guess():
    game_data = session['game_data']
    if request.method == 'POST':
        action = request.form['action']
        if action == "Imposter Guess":
            guessed_word = request.form['guessed_word']
            if guessed_word.strip().lower() == game_data['normal_word'].lower():
                game_data['imposter_guess_result'] = "correct"
            else:
                game_data['imposter_guess_result'] = "incorrect"
            session.modified = True
            return redirect(url_for('game_result'))
    return render_template("imposter_guess.html", game_info=session.get('game_data'))



@app.route("/game_result", methods=['POST', 'GET'])
def game_result():
    game_data = session['game_data']
    if request.method == 'POST':
        #store the word in the session for the next game, this is used to make sure that the same word is not generated in the next game
        if not session.get('previous_words'):
            previous_words = [game_data['normal_word']]
        else:
            previous_words = session['previous_words']
            previous_words.append(game_data['normal_word'])
        session.pop('game_data', None)
        session['previous_words'] = previous_words[-20:] #store last 20 cause session max is 4kb
        session.modified = True
        return redirect(url_for('index'))
        
    if game_data['most_voted_player'] not in game_data['imposter_names']:
        game_data['game_result'] = "Imposters Win"
    else:
        if game_data['imposter_guess_result'] == "correct":
            game_data['game_result'] = "Imposters Win"
        else:
            game_data['game_result'] = "Citizens Win"
    return render_template("game_result.html", game_info=session.get('game_data'))

@app.route("/error")
def error():
    #maybe validation can be done here
    if 'error' in session:
        #clear error message
        error_message = session['error']
        session.pop('error', None)
        return render_template("error.html", error=error_message)
    return render_template("error.html", error="An unknown error occurred. Please try again later.")




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True) #make flask available to the world and set debug to true for development


