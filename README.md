GamersGateway
This app solves gamer block through allowing the user to randomly generate a game from a list of 1000 games with the click of a button, the apply will return the name, developer, platforms available, description, trailer, and ingame images, and box art
To use the app on your device the following API are needed to be installed on the terminal
- Flask: pip install Flask
- BeautifulSoup4: pip install beautifulsoup4

How to use the app 
- To access open the folder name folder to run GamersGateway
- open both the template folder then index file and the file called fileusedtorunapp
- when running it from vs code ctrl click the url within the terminal
- should look like this: http://127.0.0.1:5000
- when open you will see a random game with the trailer, and cover art image, along with a carousel of other images
- to show the description click the turquoise button SHow/Hide description
- if you wish to generate a new game click on the generate game button
- with the trailer you can enter fullscreen through the bottom right corner of the actual trailer preview box
- to Use the carsouel click on the left and right arrows to move between. However the carsouel will change images by itself on a timer

Image preview of the app 
![image](https://github.com/Ethan-Hammond/HSC-Major-Work-SDD/assets/150311835/bd250f32-89bc-49bf-8827-905b4e7689ee)

The progam license is under an open source anyone can access the source code and change it
Source for information can be found through the URLs below:
- https://steamspy.com/api.php?request=all - URL for steam Appid, name, dev
- https://store.steampowered.com/api/appdetails?appids=%7Bappid%7D - used for trailer, ingame screenshots, description, and available platforms
- also used bing for box art image
  
 
