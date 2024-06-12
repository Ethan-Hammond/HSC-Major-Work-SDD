from flask import Flask, jsonify, request, Blueprint, render_template
import sys
import requests
import json
import random
from flask import redirect, url_for
from bs4 import BeautifulSoup
import re
# https://api.steampowered.com/ISteamApps/GetAppList/v2/
main = Blueprint('main', __name__)

def source_data():
    global random_game, json_data
    x = requests.get('https://steamspy.com/api.php?request=all') # getting the data from the api
    print(type(x.text))
    json_data = json.loads(x.text) # converting the data to json
    ## creating dictonaries for the data inside of one big dictionary using
    ##json data to easily manuver through the data
    random_game = random.choice(list(json_data.keys()))

def fetch_developer(data):
    developer = data[str(appid)].get('developers', 'No developer information available.') # Get the 'developers' field from the data
    return developer

def fetch_game_description(appid):
    global data, required_description
    url = f'https://store.steampowered.com/api/appdetails?appids={appid}'
    response = requests.get(url)  # Send a GET request to the URL
    if response.status_code == 200: # Check if the response is successful
        data = response.json()      # Convert the response to a JSON object
        if data[str(appid)]['success']:  # checking if the request attained the information
            required_description = data[str(appid)]['data'].get('detailed_description', 'no description available') # Get the 'about_the_game' field from the data
            return required_description
    return 'No description available.' # Return this message if the request was unsuccessful

def fetch_game_trailer(data, appid):
    trailers = data[str(appid)]['data'].get('movies', [])
    if trailers:
        for trailer in trailers:
            trailer_url = trailer.get('webm', {}).get('max', '')  # Ensure the URL is correctly accessed
            if not trailer_url:
                trailer_url = trailer.get('mp4', {}).get('max', '')  # Fallback to mp4 if webm is not available
            if trailer_url:
                return trailer_url
    return ""

    

## class to store the data of the game
class game_data:
    def __init__(self, appid, name, developer, description, trailer ):
        self.appid = appid
        self.name = name
        self.developer = developer
        self.description = description
        self.trailer = trailer
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
    def get_trailer(self):
        return self.trailer

source_data()





## a random game generator to help with gamer block
# the scraper used to get the image of the game
import requests
from bs4 import BeautifulSoup
 
def search_game_image(game_name):
    query = game_name + " game box art"
    url = f"https://www.bing.com/images/search?q={query}&form=QBLH"  # Bing Image Search URL
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
 
    response = requests.get(url, headers=headers) # Send a GET request to the URL
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the first image result
        image_results = soup.find_all('a', class_='iusc')
        if image_results:
            first_image_data = image_results[0]['m']
            # The 'm' attribute contains JSON-like data; we need to extract the image URL
            first_image_url = first_image_data.split('"murl":"')[1].split('","')[0]
            
        else:
            print('No image found.')
    else:
        print(f"Failed to connect. Status code: {response.status_code}")
    return first_image_url



## Diffferent routes start here


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_page():
    return render_template('base.html')

@app.route('/generator_page', methods=['GET'])
def game_suggest(): 
    global appid
    random_game = random.choice(list(json_data.keys())) 
    appid = random_game  # appending all the information to the game and creating the object for it
    description = fetch_game_description(appid)
    trailer = fetch_game_trailer(data, appid)
    developer = fetch_developer(data)
    game = game_data(appid, json_data[random_game]['name'], developer, description, trailer )
    game_name = game.get_name()
    game_image = search_game_image(game_name)
   
    
    print(game_image)
    # rendering the game page with the information
    return render_template('generator_page.html', game_name=game_name, game_image=game_image, game_description=game.get_description(), game_trailer=game.get_trailer())
@app.route('/save_game', methods=['POST'])
def save_game():
    pass


 



if __name__ == '__main__':
    app.run(debug=True)
    