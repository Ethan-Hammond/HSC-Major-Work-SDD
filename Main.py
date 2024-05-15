from flask import Flask, jsonify, request, Blueprint, render_template
import sys
import requests
import json
import random
from flask import redirect, url_for



main = Blueprint('main', __name__)

def source_data():
    global random_game, json_data
    x = requests.get('https://steamspy.com/api.php?request=all')

    print(type(x.text))
    json_data = json.loads(x.text)
    ## creating dictonaries for the data inside of one big dictionary using
    ##json data to easily manuver through the data

    random_game = random.choice(list(json_data.keys()))
    print(json_data[random_game])

   


class game_data:
    def __init__(self, appid, name, developer):
        self.appid = appid
        self.name = name
        self.developer = developer
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
game = game_data(random_game, json_data[random_game]['name'], json_data[random_game]['developer'])
# print(game.get_developer())



## a random game generator to help with gamer block
# the scraper used to get the image of the game
import requests
from bs4 import BeautifulSoup
 
def search_game_image(game_name):
    query = game_name + " game box art"
    url = f"https://www.bing.com/images/search?q={query}&form=QBLH"
 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
 
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the first image result
        image_results = soup.find_all('a', class_='iusc')
        if image_results:
            first_image_data = image_results[0]['m']
            # The 'm' attribute contains JSON-like data; we need to extract the image URL
            first_image_url = first_image_data.split('"murl":"')[1].split('","')[0]
            #print(f'Image URL: {first_image_url}')
        else:
            print('No image found.')
    else:
        print(f"Failed to connect. Status code: {response.status_code}")
    return first_image_url
game_name = game.get_name()
search_game_image(game_name)



## Diffferent routes start here


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_page():
    return render_template('base.html')

@app.route('/generator_page', methods=['GET'])
def game_suggest():
    random_game = random.choice(list(json_data.keys()))
    game = game_data(random_game, json_data[random_game]['name'], json_data[random_game]['developer'])
    game_name = game.get_name()
    game_image = search_game_image(game_name)
    print(game_image)
    return render_template('generator_page.html', game_name=game_name, game_image=game_image)
@app.route('/save_game', methods=['POST'])
def save_game():
    pass


 



if __name__ == '__main__':
    app.run(debug=True)
    