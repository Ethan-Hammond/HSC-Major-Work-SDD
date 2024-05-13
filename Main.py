from flask import Flask, jsonify, request, Blueprint, render_template
import sys
import requests
import json
import random
from flask import redirect, url_for


main = Blueprint('main', __name__)

def source_data():
    global random_game, json_data
    x = requests.get('https://steamspy.com/api.php?request=all&page=1')

    print(type(x.text))
    json_data = json.loads(x.text)
    ## creating dictonaries for the data inside of one big dictionary using
    ##json data to easily manuver through the data

    random_game = random.choice(list(json_data.keys()))
    print(json_data[random_game])
   


class game_data:
    def __init__(self, appid, name, developer, genre, price, rating):
        self.appid = appid
        self.name = name
        self.developer = developer
        self.genre = genre
        self.price = price
        self.rating = rating
    def get_name(self):
        return self.name    # returns the name of the game
    def get_data(self):
        return self.data   # returns the data of the game
    def get_developer(self):
        return self.developer   # returns the developer of the game
    def get_genre(self):
        return self.genre  # returns the genre of the game
    def get_price(self):
        return self.price  # returns the price of the game
    def get_rating(self):
        return self.rating  # returns the rating of the game

source_data()
game = game_data(random_game, json_data[random_game]['name'], json_data[random_game]['developer'], json_data[random_game]['price'], json_data[random_game]['positive'], json_data[random_game]['score_rank'])
print(game.get_name())
print(game.get_developer())



## a random game generator to help with gamer block






## Diffferent routes start here


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_page():
    return render_template('base.html')

@app.route('/generator_page', methods=['GET'])
def game_suggest():
    random_game = random.choice(list(json_data.keys()))
    game = game_data(random_game, json_data[random_game]['name'], json_data[random_game]['developer'], json_data[random_game]['price'], json_data[random_game]['positive'], json_data[random_game]['score_rank'])
    return jsonify({"game": game.get_name(), "developer": game.get_developer()}), render_template('generator.html')

@app.route('/save_game', methods=['POST'])
def save_game():
    pass


if __name__ == '__main__':
    app.run(debug=True)
    