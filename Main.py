from flask import Flask, jsonify, request
import random
import sys
import requests
import json
import random
from flask import Flask, jsonify, request



def source_data():
    global random_game, json_data
    x = requests.get('https://steamspy.com/api.php?request=all&page=1')

    print(type(x.text))
    json_data = json.loads(x.text)
    ## creating dictonaries for the data inside of one big dictionary using
    ##json data to easily manuver through the data
# randomly selecting a game from the dictonary of games

    random_game = random.choice(list(json_data.keys()))
    print(json_data[random_game])
   


class game_data:
    def __init__(self, appid, name, developer, genre, price, rating):
        self.appid = appid  #setting up each attribute for data to be stored
        self.name = name
        self.developer = developer
        self.genre = genre
        self.price = price
        self.rating = rating
    def get_name(self):
        return self.name
    def get_data(self):
        return self.data
    def get_developer(self):
        return self.developer
    def get_genre(self):
        return self.genre
    def get_price(self):
        return self.price
    def get_rating(self):
        return self.rating

source_data()
#applying each attribute the required data from the dictonary
#and assigning it a variable to be called upon
game = game_data(random_game, json_data[random_game]['name'], json_data[random_game]['developer'], json_data[random_game]['price'], json_data[random_game]['positive'], json_data[random_game]['score_rank'])
print(game.get_name())
print(game.get_developer())



## a random game generator to help with gamer block

app = Flask(__name__)

# initiallising the webapp access point 
@app.route('/suggest', methods=['GET'])
def suggest():
    random_game = random.choice(list(json_data.keys()))
    game = game_data(random_game, json_data[random_game]['name'], json_data[random_game]['developer'], json_data[random_game]['price'], json_data[random_game]['positive'], json_data[random_game]['score_rank'])
    return jsonify({"game": game.get_name(), "developer": game.get_developer()})

if __name__ == '__main__':
    app.run(debug=True)
                
