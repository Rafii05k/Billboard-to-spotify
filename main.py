import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("which year you would like to travel to? write in YYY-MM-DD format. ")
billboard_url = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(billboard_url)
soup = BeautifulSoup(response.text, "html.parser")
song_names_span = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_span]
print(song_names)
# client ID and secrete from the spotify app I created
client_id = "6edcea71b4c8462f8c5200ae84df5d9f"
client_secret = "2ef4b09f51d94c3eba8ff2159af77155"
redirect_uri = "http://localhost:8888/callback"
scope = 'playlist-modify-public'  # or 'playlist-modify-private' depending on your needs
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))
user = sp.current_user()
user_id = sp.current_user()['id']

# Create a new playlist
playlist_name = f"Top 100 Billboard Songs on  {date}"
playlist_description = f"A playlist containing the top 100 songs from Billboard on  {date}."
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=playlist_description)
playlist_id = playlist['id']

# searches for each song of the billboard
def get_song_uri(sp, song_name):
    results = sp.search(q=f"track:{song_name}", type='track', limit=1)
    return results['tracks']['items'][0]['uri'] if results['tracks']['items'] else None

# Collect song URIs using list comprehension
song_uris = [get_song_uri(sp, song) for song in song_names if get_song_uri(sp, song)]

# Add songs to the playlist
if song_uris:
    sp.playlist_add_items(playlist_id, song_uris)
    print(f"Added {len(song_uris)} songs to the playlist.")
else:
    print("No songs found on Spotify.")






