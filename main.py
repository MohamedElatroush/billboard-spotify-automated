import os

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth

year = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{year}/"
response = requests.get(URL)

html = response.text

soup = BeautifulSoup(html, "html.parser")

music = soup.select(selector="li ul li h3")

songs = [song.text.strip("\n\t") for song in music]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    redirect_uri="http://example.com",
    client_id=os.environ["SPOTIFY_CLIENT_ID"],
    client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
    show_dialog=True,
    cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
song_uris = []
year = year.split("-")[0]
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, public=False, name=f"{year} BillBoard 100")
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)