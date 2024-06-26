from flask import Flask, render_template, request
import requests
import json
import random
from bs4 import BeautifulSoup

app = Flask(__name__)

def source_data():
    global random_game, json_data, appid
    x = requests.get('https://steamspy.com/api.php?request=all')
    json_data = json.loads(x.text) # converting the data to json
    ## creating dictonaries for the data inside of one big dictionary using
    ##json data to easily manuver through the data
    random_game = random.choice(list(json_data.keys()))
    

source_data()

def fetch_game_trailer(appid):
        trailers =  data[str(appid)]['data'].get('movies', [])
        trailer_url = ""
        if trailers:
            trailer = trailers[0]
            trailer_url = trailer.get('webm', {}).get('max', '') or trailer.get('mp4', {}).get('max', '') # Ensure the URL is correctly accessed


            return trailer_url
        return 'Unknown Game', 'No trailer available.', ''



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
    query = game_name + " game box art" # Append 'game box art' to the game name to get relevant images
    url = f"https://www.bing.com/images/search?q={query}&form=QBLH"  # Bing Image Search URL
    # set the headers to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    } 
    response = requests.get(url, headers=headers)
    if response.status_code == 200: # Check if the response is successful
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
    platforms = data[str(appid)]['data'].get('platforms', {}) # Get the 'platforms' field from the data
    supported_platforms = [] # Create an empty list to store the supported platforms 
    for platform, is_supported in platforms.items():
        if is_supported: # Check if the platform is supported
            supported_platforms.append(platform) # Return the supported platforms
    return ', '.join(supported_platforms)

def ingame_images(appid):
    images = data[str(appid)]['data'].get('screenshots', []) # Get the 'screenshots' field from the data
    image_urls = [] # Create an empty list to store the image URLs
    for image in images:
        image_url = image.get('path_thumbnail', '') # Get the 'path_thumbnail' attribute of the image
        if image_url: # Check if the URL is not empty
            image_urls.append(image_url) # Add the URL to the list
    return image_urls
class game_data:
    def __init__(self, appid, name, developer, description, trailer, platforms ):
        self.appid = appid
        self.name = name
        self.developer = developer
        self.description = description
        self.trailer = trailer
        self.platforms = platforms
    def get_name(self):
        return self.name    # returns the name of the game
    def get_data(self):
        return self.data   # returns the data of the game
    def get_developer(self):
        return self.developer   # returns the developer of the game
    def get_genre(self):
        return self.genre  # returns the genre of the game
    def get_description(self):
        return self.description
    def get_trailer(self):
        return self.trailer
    def get_platforms(self):
        return self.platforms
    

# The main route of the application that renders the index.html template and passes the game data into a class object to be displayed
@app.route('/')
def index():
    global appid
    random_game = random.choice(list(json_data.keys()))
    appid = random_game
    description = fetch_game_description(appid)
    trailer = fetch_game_trailer(appid)
    platforms = find_platforms(appid)
    game = game_data(appid, json_data[random_game]['name'], json_data[random_game]['developer'], description, trailer, platforms) 
    game_name = game.get_name()
    game_developer = game.get_developer()
    game_image = search_game_image(game_name)
    game_ingame_images = ingame_images(appid)
    return render_template('index.html', game_ingame_images=game_ingame_images, game_description=game.get_description(), game_name=game_name, game_developer=game_developer, game_image=game_image, game_trailer=game.get_trailer(), platforms=game.get_platforms())  

if __name__ == '__main__':
    app.run(debug=True)
