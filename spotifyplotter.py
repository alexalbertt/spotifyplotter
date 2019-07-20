from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import spotipy
from PIL import Image
import client
from operator import itemgetter

# input API keys here
client_credentials_manager = SpotifyClientCredentials(client_id=client.client_id, client_secret=client.client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# pick the text file to load
genre = input("Top 100, country, rap, or pop? (t, c, r or p)").lower()
if genre == "t":
    file_name = "billboard_top_100/billboard_top_100.txt"
    title = "BillBoard Top 100 Artists"
elif genre == "c":
    file_name = "top_country/top_country.txt"
    title = "Top Country Artists"
elif genre == "r":
    file_name = "top_rap/top_rap.txt"
    title = "Top Rap Artists"
elif genre == "p":
    file_name = "top_pop/top_pop.txt"
    title = "Top Pop Artists"
else:
    print("Error, not a genre.")

#insert file name
f = open(f"artist_txt_files/{file_name}", "r")

# add each artist to list
fl =f.readlines()
artists = []
for x in fl:
    artists.append(x.rstrip('\n'))


artist_values = {}
for x in artists:
    danceability_avg = 0
    try:
        results = sp.search(q=x, limit=20)
        tids = []
        for i, t in enumerate(results['tracks']['items']):
            tids.append(t['uri'])
            id = t['uri'].split(":")[2]

            features = sp.audio_features(id)
            danceability = round(features[0]['danceability'], 3)
            danceability_avg += danceability
        danceability_avg /= 20
        print(x + ":", danceability_avg)
        artist_values[x] = round(danceability_avg, 3)
    except:
        print(x, "error")
print(artist_values)



# sort the values
artist_values_sorted_list = sorted(artist_values.items(), key=itemgetter(1), reverse=False)
artist_values_sorted = {}
for i in artist_values_sorted_list:
    artist_values_sorted[i[0]] = i[1]
my_range=range(1,len(artists)+1)

# change color and shape and size and edges
plt.style.use('dark_background')
plt.hlines(y=my_range, xmin=0, xmax=np.array(list(artist_values_sorted.values())), color='limegreen')
plt.plot(np.array(list(artist_values_sorted.values())), my_range, "og", markersize=3)
plt.yticks(my_range, artist_values_sorted.keys())
plt.title(f"Danceability Scores of {title}")
plt.ylabel("Artist")
plt.xlabel("Danceability Score")
plt.tick_params(axis='y', which='major', labelsize=4)
plt.xlim(left=0, right=1)
plt.margins(y=.01)
plt.tight_layout()
plt.show()

# screenshot_name = input("Screenshot file name: ")
# im = Image.open(screenshot_name)
# isize = im.size
# rgb_im = im.convert('RGB')
# for x in range(0, isize[0]):
#     for y in range(0, isize[1]):
#         r, g, b = rgb_im.getpixel((x,y))
#         if r == 247 and g == 32:
#             print(r, g, b)
#             new_im = Image.new("RGB", (20,20), (255,255,255))
#             rgb_im.paste(new_im, (x-3, y-3))
# rgb_im.show()
