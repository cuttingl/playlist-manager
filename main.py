from pip import main
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import json


def search_artist():
    load_dotenv('secret.env')
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=os.getenv('CLIENT_ID'),client_secret=os.getenv('CLIENT_SECRET')))

def getPlaylists():
    load_dotenv('secret.env')
    tab_playlist = []
    
    playlist_ids = {"name" : "", "id" : ""}
    scope = 'playlist-read-private'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),client_secret=os.getenv('CLIENT_SECRET'),redirect_uri="http://localhost",scope=scope))

    results = sp.current_user_playlists(limit=50)
    
    for i, item in enumerate(results['items']):
        if item["name"] == "Release Radar" or item["name"] == "Discover Weekly":
            playlist_ids["name"] = item['name']
            playlist_ids["id"] = item['id']
            tab_playlist.append(playlist_ids.copy())
    
    print(tab_playlist)
    
def tracks_in_playlist():
    pass 

if __name__ == '__main__':
    getPlaylists()