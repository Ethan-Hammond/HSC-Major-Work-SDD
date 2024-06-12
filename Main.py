from flask import Flask, jsonify, request, Blueprint, render_template
import sys
import requests
import json
import random
import sys

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

games = ["Minecraft", "Fortnite", "Apex Legends", "League of Legennds", "Call of Duty"]


@app.route('/suggest', methods=['GET'])
def suggest_game():
    game = random.choice(games)
    return jsonify({"suggested_game": game}, "Ethan")

if __name__ == '__main__':
    app.run(debug=True)
    