from flask import Flask, jsonify, request, Blueprint, render_template
import sys
import requests
import json
import random
from flask import redirect, url_for
from bs4 import BeautifulSoup


main = Blueprint('main', __name__)

def source_data():
    global random_game, json_data
    x = requests.get('https://steamspy.com/api.php?request=all')
    print(type(x.text))
    json_data = json.loads(x.text)
    ## creating dictonaries for the data inside of one big dictionary using
    ##json data to easily manuver through the data
    random_game = random.choice(list(json_data.keys()))



def fetch_game_description(appid):
    url = f'https://store.steampowered.com/api/appdetails?appids={appid}'
    response = requests.get(url)  # Send a GET request to the URL
    if response.status_code == 200: # Check if the response is successful
        data = response.json()      # Convert the response to a JSON object
        if data[str(appid)]['success']:  # checking if the request attained the information
            return render_template(data[str(appid)]['data'].get('detailed_description', 'no description available')) # Get the 'about_the_game' field from the data
    return 'No description available.' # Return this message if the request was unsuccessful

# def clean_html(raw_html):
#     soup = BeautifulSoup(raw_html, 'html.parser')
#     soup.get_text()
#     description = ['data'].get('about_the_game', 'No description available.')
#     return soup(description)
    
## class to store the data of the game
class game_data:
    def __init__(self, appid, name, developer, ):
        self.appid = appid
        self.name = name
        self.developer = developer
        #self.description = description
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
    def get_description(self):
        return self.description

source_data()

game = game_data(random_game, json_data[random_game]['name'], json_data[random_game]['developer'],)
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
    global appid
    random_game = random.choice(list(json_data.keys()))
    appid = random_game
    description = fetch_game_description(appid)
    game = game_data(appid, json_data[random_game]['name'], json_data[random_game]['developer'], description )
    game_name = game.get_name()
    game_image = search_game_image(game_name)
    
    print(game_image)
    return render_template('generator_page.html', game_name=game_name, game_image=game_image, game_description=game.get_description())
@app.route('/save_game', methods=['POST'])
def save_game():
    pass


 



if __name__ == '__main__':
    app.run(debug=True)
    