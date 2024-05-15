import cloudscraper
from bs4 import BeautifulSoup

# URL of the webpage you want to scrape
url = 'https://steamdb.info/app/601150/'  # replace with the actual URL

# Create a cloudscraper instance
scraper = cloudscraper.create_scraper()

# Send a GET request to the webpage
response = scraper.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first element with the class 'app-logo'
    img_tag = soup.find('img', class_='app-logo')

    # Check if an img tag was found
    if img_tag:
        # Get the URL from the 'src' attribute
        img_url = img_tag.get('src')
        print(f'Image URL: {img_url}')
    else:
        print('No image with class "app-logo" found.')
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
