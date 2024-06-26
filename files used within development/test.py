import cloudscraper
from lxml import html

url = "https://steamdb.info/app/601150/"

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Cookie': 'Here is where I copied the cookies from my browser, I looked through it and it contained some info that Might be able to personally identify me so I removed it from the post',
    'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': "Windows",
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

if __name__ == "__main__":
    scraper = cloudscraper.CloudScraper()
    scraper.headers = HEADERS
    page = scraper.get(url, timeout=100000)

    if page.status_code == 200:
        print("Successfully connected")

        # Parse the HTML content
        tree = html.fromstring(page.content)

        # Find the image tag with the class 'app-logo'
        img_tag = tree.xpath('//img[contains(@class, "app-logo")]')

        if img_tag:
            # Get the URL from the 'src' attribute
            img_url = img_tag[0].get('src')
            print(f'Image URL: {img_url}')
        else:
            print('No image with class "app-logo" found.')
    else:
        print(f"Failed to connect. Status code: {page.status_code}")