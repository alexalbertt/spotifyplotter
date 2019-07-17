import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import spotipy
from PIL import Image
import time

artists = ["Eminem", "Kendrick Lamar", "J. Cole", "Travis Scott", "Logic",
            "Juice WRLD", "Drake", "Post Malone", "Lil Wayne", "A Boogie",
            "21 Savage", "Migos", "Joyner Lucas", "Tyler, the Creator", "Lil Baby",
            "J.I.D", "Meek Mill", "Kanye West", "Playboi Carti", "Denxel Curry",
            "Future", "DaBaby", "Lil Nas X", "Rich the Kid", "Young Thug"]
# create data
artist_values = {}
for i in artists:
    artist_values[i] = np.random.randint(1,101)
values=np.random.uniform(size=40)
my_range=range(1,len(artists)+1)
print(values)

color = colors.to_rgb("r")
# change color and shape and size and edges
plt.style.use('dark_background')
plt.hlines(y=my_range, xmin=0, xmax=list(sorted(artist_values.values())), color='limegreen')
plt.plot(list(sorted(artist_values.values())), my_range, "or")
plt.yticks(my_range, artists)
plt.ylabel("Rapper")
plt.xlabel("Danceability Level")

plt.show(block=False)
screenshot_name = input("Screenshot file name: ")
im = Image.open(screenshot_name)
isize = im.size
rgb_im = im.convert('RGB')
for x in range(0, isize[0]):
    for y in range(0, isize[1]):
        r, g, b = rgb_im.getpixel((x,y))
        if r == 247 and g == 32:
            print(r, g, b)
            new_im = Image.new("RGB", (20,20), (255,255,255))
            rgb_im.paste(new_im, (x-3, y-3))
rgb_im.show()
