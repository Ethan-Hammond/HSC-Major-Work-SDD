import steamspypi
import random
import sys

def get_appids():
    global appids,game_name
    data_request = dict()
    data_request['request'] = 'all'
    data_request['page'] = '0'

    data = steamspypi.download(data_request)

    appids = []
    for appid, app_data in data.items():
        appids.append(appid)
        
    game = random.choice(appids)
    game_name = data[game]

    return appids, game_name

class api_call:
    def __init__(self, appid):
        self.appid = appid
        self.data = steamspypi.download(appid)
    def get_data(self):
        return self.data

class get_game_data:
    def __init__(self, appid,):
        self.appid = appid
        self.data = steamspypi.download(appid)





class gamer:
    def __init__(self, name, developer, genre, price, rating, appid):
        self.name = name
        self.developer = developer
        self.genre = genre
        self.price = price
        self.rating = rating
        self.appid = appid
        self.games = []
    def add_game(self, game):
        self.games.append(game_name)
    def get_games(self):
        return self.games




get_appids()
print(game_name)

