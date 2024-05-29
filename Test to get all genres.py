import requests
from bs4 import BeautifulSoup

def fetch_steam_genres():
    url = 'https://store.steampowered.com/tag/browse/#global_492'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    genres = {}
    for tag in soup.select('.tag_browse_tag'):
        genre_name = tag.text.strip()
        genre_id = tag['data-tagid']
        genres[genre_name] = genre_id
    
    return genres

# Example usage
genres = fetch_steam_genres()
for genre, genre_id in genres.items():
    print(f"{genre}: {genre_id}")
