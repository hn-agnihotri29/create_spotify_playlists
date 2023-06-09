import html
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests


CLIENT_ID = "d1612a0c952a4c2298f0fcde55950dfb"
CLIENT_Secret = "eb0e922407b447c8936849faa51c8940"
URL = "http://example.com/?code=AQBjmAf4ci4fqhMryKyRm2borkAUfPiCba-4zCQ-Q7VtDPcH3T_shYbspDntS-zCFtc3863L-HSNnuY_ju-N_jiXQMD1l-GTCHpmij63Q_a_oCNpCPipCA0GX8Zs_NWng9_u6BwnCUvFEBWtt6gVeQWF_t6iT858YjK4WjiLtYXSVtVIUxmq2HB7lcZnqVY"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)

BILLBOARD_LIST = "https://www.billboard.com/charts/hot-100"


user_id = sp.current_user()["id"]

# Billboard 100 music list

date = input("Which year do you want to travel to? Type the date in format YYYY-MM-DD: ")

billboard_song_list = requests.get(f"{BILLBOARD_LIST}/{date}/").text
soup = BeautifulSoup(billboard_song_list, "html.parser")
music_tags = soup.find_all(name="h3", class_="a-no-trucate")
top_songs_list = [html.unescape(music.getText()).strip() for music in music_tags]

year = date.split("-")[0]

# Spotify

song_uris = []
for song in top_songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)







