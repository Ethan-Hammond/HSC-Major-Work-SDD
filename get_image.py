import requests
import json
import random

def search_game():
    search_term = input("Enter the name of the game you want to search for: ")
    url = f"https://store.steampowered.com/api/storesearch/?term={search_term}&l=english&cc=AU"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        games = data['items']
        game = random.choice(games)
        appid = game['id']
        name = game['name']
        platforms = game['platforms']
        return appid, name, platforms
    return None, None, None

print(search_game())