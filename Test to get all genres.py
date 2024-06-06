import requests
from bs4 import BeautifulSoup

def fetch_steam_genres():
    url = 'https://store.steampowered.com/tag/browse/#global_492'
    response = requests.get(url)       # Send a GET request to the URL
    response.raise_for_status()       # Ensure the response is successful
    soup = BeautifulSoup(response.content, 'html.parser') # Parse the HTML content of the page
    
    genres = {}
    for tag in soup.select('.tag_browse_tag'): # Select all tags with the class 'tag_browse_tag'
        genre_name = tag.text.strip()  # Get the text content of the tag
        genre_id = tag['data-tagid']  # Get the 'data-tagid' attribute of the tag
        genres[genre_name] = genre_id # Add the genre to the dictionary
    
    return genres

# Example usage
genres = fetch_steam_genres()
for genre, genre_id in genres.items():  # Loop through the genres and print them
    print(f"{genre}: {genre_id}")
