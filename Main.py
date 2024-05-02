from flask import Flask, jsonify, request
import random
import sys

## a random game generator to help with gamer block

app = Flask(__name__)

games = ["Minecraft", "Fortnite", "Apex Legends", "League of Legennds", "Call of Duty"]


@app.route('/suggest', methods=['GET'])
def suggest_game():
    game = random.choice(games)
    return jsonify({"suggested_game": game}, "Ethan")

if __name__ == '__main__':
    app.run(debug=True)
                
