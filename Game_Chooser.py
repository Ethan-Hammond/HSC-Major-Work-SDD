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
game = game_data(random_game, json_data[random_game]['name'], json_data[random_game]['developer'], json_data[random_game]['price'], json_data[random_game]['positive'], json_data[random_game]['score_rank'])
print(game.get_name())
print(game.get_developer())