from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import spotipy
import client
from operator import itemgetter

# input API keys here
client_credentials_manager = SpotifyClientCredentials(client_id=client.client_id, client_secret=client.client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def txt_picker():
    # pick the text file to load
    while True:
        feature = input("Display danceability, energy or loudness? (d, e or l)")
        if feature == "d":
            feature = "Danceability"
        elif feature == "e":
            feature = "Energy"
        elif feature == "l":
            feature = "Loudness"
        else:
            print("Error, not a type. Try again.")
            pass

        genre = input("Top 100, country, rap, or pop? (t, c, r or p)").lower()
        if genre == "t":
            file_name = "billboard_top_100/billboard_top_100.txt"
            title = "BillBoard Top 100 Artists"
            return title, file_name, feature
        elif genre == "c":
            file_name = "top_country/top_country.txt"
            title = "Top Country Artists"
            return title, file_name, feature
        elif genre == "r":
            file_name = "top_rap/top_rap.txt"
            title = "Top Rap Artists"
            return title, file_name, feature
        elif genre == "p":
            file_name = "top_pop/top_pop.txt"
            title = "Top Pop Artists"
            return title, file_name, feature
        else:
            print("Error, not a genre. Try again.")

def add_artists(file_name):
    #insert file name
    f = open(f"artist_txt_files/{file_name}", "r")

    # add each artist to list
    fl =f.readlines()
    artists = []
    for x in fl:
        artists.append(x.rstrip('\n'))
    return artists

def get_feature_scores(artists, feature):
    artist_values = {}
    for x in artists:
        score_avg = 0
        try:
            results = sp.search(q=x, limit=20)
            tids = []
            for i, t in enumerate(results['tracks']['items']):
                tids.append(t['uri'])
                id = t['uri'].split(":")[2]

                features = sp.audio_features(id)
                score = round(features[0][feature.lower()], 3)
                score_avg += score
            score_avg /= 20
            print(x + ":", score_avg)
            artist_values[x] = round(score_avg, 3)
        except:
            print(x, "error")
    return(artist_values)


def sort_values(artist_values):
    # sort the values
    artist_values_sorted_list = sorted(artist_values.items(), key=itemgetter(1), reverse=False)
    artist_values_sorted = {}
    for i in artist_values_sorted_list:
        artist_values_sorted[i[0]] = i[1]
    return artist_values_sorted

def display_plot(artist_values_sorted, title, feature):
    # change color and shape and size and edges
    my_range=range(1,len(artist_values_sorted)+1)
    plt.style.use('dark_background')
    plt.hlines(y=my_range, xmin=0, xmax=np.array(list(artist_values_sorted.values())), color='limegreen')
    plt.plot(np.array(list(artist_values_sorted.values())), my_range, "og", markersize=3)
    plt.yticks(my_range, artist_values_sorted.keys())
    plt.title(f"{feature} Scores of {title}")
    plt.ylabel("Artist")
    plt.xlabel(f"{feature} Score")
    plt.tick_params(axis='y', which='major', labelsize=4)
    plt.xlim(left=0, right=1)
    plt.margins(y=.01)
    plt.tight_layout()
    plt.show()

def main():
    title, file_name, feature = txt_picker()
    artists = add_artists(file_name)
    artist_values = get_feature_scores(artists, feature)
    artist_values_sorted = sort_values(artist_values)
    display_plot(artist_values_sorted, title, feature)

if __name__ == "__main__":
    main()
