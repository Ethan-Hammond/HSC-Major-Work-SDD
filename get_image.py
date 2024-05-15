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
            print(f'Image URL: {first_image_url}')
        else:
            print('No image found.')
    else:
        print(f"Failed to connect. Status code: {response.status_code}")
 
# Example usage
game_name = "Devil May Cry 5"
search_game_image(game_name)
