from dataclasses import dataclass
from pip import main
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import json
from datetime import date


def search_artist():
    load_dotenv('secret.env')
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=os.getenv('CLIENT_ID'),client_secret=os.getenv('CLIENT_SECRET')))

def getPlaylists(playlists):
    load_dotenv('secret.env')
    
    playlist_ids = {"name" : "", "id" : ""}
    scope = 'playlist-read-private'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),client_secret=os.getenv('CLIENT_SECRET'),redirect_uri="http://localhost",scope=scope))

    results = sp.current_user_playlists(limit=50)
    
    for i, item in enumerate(results['items']):
        if item["name"] == "Release Radar" or item["name"] == "Discover Weekly":
            playlist_ids["name"] = item['name']
            playlist_ids["id"] = item['id']
            playlists.append(playlist_ids.copy())
    
def tracks_in_playlist(playlists, name, tracks):
    load_dotenv('secret.env')
    scope = 'playlist-read-private'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),client_secret=os.getenv('CLIENT_SECRET'),redirect_uri="http://localhost",scope=scope))
    tracks_ids = {"name" : "", "id" : ""}
    
    for playlist in playlists:
        if playlist["name"] == name:
            results = sp.playlist_items(playlist['id'])
            for i, item in enumerate(results['items']):
                tracks_ids["name"] = item['track']['name']
                tracks_ids["id"] = item['track']["id"]
                tracks.append(tracks_ids.copy())
    return tracks

def add_tracks_to_playlist(tracks, playlist_name):
    load_dotenv('secret.env')
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),client_secret=os.getenv('CLIENT_SECRET'),redirect_uri="http://localhost",scope=scope))
    
    user_id = sp.me()['id']
    sp.user_playlist_create(user_id, playlist_name, public=True)
    
    new_playlist = sp.current_user_playlists(limit=1)
    playlist_id = new_playlist["items"][0]["id"]
    for track in tracks :
        sp.playlist_add_items(playlist_id, [track["id"]])
    

if __name__ == '__main__':
    today = date.today()
    d4 = today.strftime("%b-%d-%Y")
    playlists = []
    getPlaylists(playlists)
    
    tracks_rr = []
    tracks_dw = []
    tracks_rr = tracks_in_playlist(playlists, "Release Radar", tracks_rr)
    tracks_dw = tracks_in_playlist(playlists, "Discover Weekly", tracks_dw)

    add_tracks_to_playlist(tracks_rr, "Release Radar " + d4)
    add_tracks_to_playlist(tracks_dw, "Discover Weekly " + d4)

    
    
    