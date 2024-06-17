from flask import Flask, render_template, request
import requests
import json
import random
from bs4 import BeautifulSoup

app = Flask(__name__)

def source_data():
    global random_game, json_data, appid
    x = requests.get('https://steamspy.com/api.php?request=all')
    json_data = json.loads(x.text)
    random_game = random.choice(list(json_data.keys()))
    

source_data()

def fetch_game_trailer(appid):
        trailers =  data[str(appid)]['data'].get('movies', [])
        trailer_url = ""
        if trailers:
            trailer = trailers[0]
            trailer_url = trailer.get('webm', {}).get('max', '') or trailer.get('mp4', {}).get('max', '')


            return trailer_url
        return 'Unknown Game', 'No description available.', ''



def fetch_game_description(appid):
    global data
    url = f'https://store.steampowered.com/api/appdetails?appids={appid}'
    response = requests.get(url)  # Send a GET request to the URL
    if response.status_code == 200: # Check if the response is successful
        data = response.json()      # Convert the response to a JSON object
        if data[str(appid)]['success']:  # checking if the request attained the information
            required_description = data[str(appid)]['data'].get('about_the_game', 'No description available.')
            # Parse the HTML to extract the text content
            soup = BeautifulSoup(required_description, 'html.parser')
            clean_description = soup.get_text(separator=' ').strip()
            return clean_description# Get the 'about_the_game' field from the data
    return 'No description available.' # Return this message if the request was unsuccessful


def search_game_image(game_name):
    query = game_name + " game box art"
    url = f"https://www.bing.com/images/search?q={query}&form=QBLH" 
    # set the headers to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    } 
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the first image result
        image_results = soup.find_all('a', class_='iusc')
        # The 'm' attribute contains JSON-like data; we need to extract the image URL
        if image_results:
            first_image_data = image_results[0]['m']
            first_image_url = first_image_data.split('"murl":"')[1].split('","')[0]
            return first_image_url
    return ""

def find_platforms(appid):
    platforms = data[str(appid)]['data'].get('platforms', {})
    x = 0
    while x < len(platforms):
        if platforms[list(platforms.keys())[x]] == True:
            return list(platforms.keys())
        x += 1
def find_price(appid):
    price = data[str(appid)]['data'].get('final_formatted', {})
    
    return price

class game_data:
    def __init__(self, appid, name, developer, description, trailer, platforms, price ):
        self.appid = appid
        self.name = name
        self.developer = developer
        self.description = description
        self.trailer = trailer
        self.platforms = platforms
        self.price = price
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
    def get_platforms(self):
        return self.platforms
    


@app.route('/')
def index():
    global appid
    random_game = random.choice(list(json_data.keys()))
    appid = random_game
    description = fetch_game_description(appid)
    trailer = fetch_game_trailer(appid)
    platforms = find_platforms(appid)
    game = game_data(appid, json_data[random_game]['name'], json_data[random_game]['developer'], description, trailer, platforms, price )
    game_name = game.get_name()
    game_image = search_game_image(game_name)
    price = find_price(appid)
    return render_template('index.html', game_description=game.get_description(), game_name=game_name, game_image=game_image, game_trailer=game.get_trailer(), platforms=game.get_platforms(), price=game.get_price())  

if __name__ == '__main__':
    app.run(debug=True)
