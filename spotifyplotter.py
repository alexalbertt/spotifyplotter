from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import spotipy
import client
from operator import itemgetter

# input API keys here
client_credentials_manager = SpotifyClientCredentials(
    client_id=client.client_id, client_secret=client.client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def txt_picker():
    """Selects audio feature type and artist genre type"""

    while True:

        # pick the feature to display
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

        # pick the genre to display
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
    """Adds artists to list from text file"""

    # insert file name
    f = open(f"artist_txt_files/{file_name}", "r")

    # add each artist to list
    fl = f.readlines()
    artists = []
    for x in fl:
        artists.append(x.rstrip("\n"))
    return artists


def get_feature_scores(artists, feature):
    """Averages the audio features from the top 20 tracks of each artist"""

    artist_values = {}
    for x in artists:
        score_avg = 0
        try:

            # fetch top 20 tracks
            results = sp.search(q=x, limit=20)
            tids = []
            for i, t in enumerate(results["tracks"]["items"]):
                tids.append(t["uri"])
                id = t["uri"].split(":")[2]

                # get the audio feature score and add it to the total
                features = sp.audio_features(id)
                score = round(features[0][feature.lower()], 3)
                score_avg += score

            # set artist equal to average score
            score_avg /= 20
            print(x + ":", score_avg)
            artist_values[x] = round(score_avg, 3)
        except:
            print(x, "error")
    return artist_values


def sort_values(artist_values):
    """Sorts the artists by their audio feature score"""

    # sort the values into a list
    artist_values_sorted_list = sorted(
        artist_values.items(), key=itemgetter(1), reverse=False
    )

    # convert list into dict
    artist_values_sorted = {}
    for i in artist_values_sorted_list:
        artist_values_sorted[i[0]] = i[1]
    return artist_values_sorted


def display_plot(artist_values_sorted, title, feature):
    """Formats and displays the matlib plot"""

    my_range = range(1, len(artist_values_sorted) + 1)
    plt.style.use("dark_background")

    # create horizontal lines
    plt.hlines(
        y=my_range,
        xmin=0,
        xmax=np.array(list(artist_values_sorted.values())),
        color="limegreen",
    )

    # create plot values and specify marker values
    plt.plot(
        np.array(list(artist_values_sorted.values())), my_range, "og", markersize=3
    )

    # add lables to plot
    plt.yticks(my_range, artist_values_sorted.keys())
    plt.title(f"{feature} Scores of {title}")
    plt.ylabel("Artist")
    plt.xlabel(f"{feature} Score")
    plt.tick_params(axis="y", which="major", labelsize=4)

    # change the range of the x axis
    plt.xlim(left=0, right=1)

    # get rid of extra margins
    plt.margins(y=0.01)
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
