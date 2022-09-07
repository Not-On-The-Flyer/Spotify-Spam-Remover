
# Written by Michelle Alberda
# Condensed version of a script we run to remove spam songs from a collaborative Spotify playlist
# It works by using feeding it a list of allowed accounts
# Uses the amazing Spotipy library by Paul Lamere (https://github.com/plamere/spotipy)

import spotipy
from spotipy import CacheFileHandler
from spotipy.oauth2 import SpotifyOAuth

# Users that are allowed to add songs
allow_list = [
    'username1',
    'username2',
    'username3'
]

# Grab PLAYLIST ID from https://open.spotify.com/playlist/<<PLAYLIST_ID>>?notneededinfo
# Do not include question mark and information that follows it
spotify_playlists = [
    'playlist_id_1',
    'playlist_id_2',
    'playlist_id_3'
]

# Create an app at https://developer.spotify.com/dashboard/ to generate this data
spotify_auth_data = {
    'spotify_scope': 'playlist-read-collaborative,playlist-modify-public,playlist-modify-private',

    # Can be found by clicking on the application in the dashboard
    'spotify_client_id': 'checkthedashboard',

    # Can be found by clicking on the application in the dashboard
    'spotify_client_secret': 'checkthedashboard',

    # Make sure the redirect URI in the Spotify console is the same ("Edit settings")
    'spotify_redirect_uri': 'http://127.0.0.1:8080'
}

# Authentication for headless server
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(open_browser=False, scope=spotify_auth_data['spotify_scope'], client_id=spotify_auth_data['spotify_client_id'],
                    client_secret=spotify_auth_data['spotify_client_secret'], redirect_uri=spotify_auth_data['spotify_redirect_uri'], cache_handler=CacheFileHandler(username='spotify')))


def spotify_spam_remover(playlist_id, allow_list):
    '''Removes songs added by users not on the allow_list'''

    # List of track URI to delete
    to_delete = []

    function_playlist = sp.playlist(playlist_id)
    items = function_playlist['tracks']['items']

    for item in items:
        if item['added_by']['id'] not in allow_list:
            to_delete.append(item['track']['uri'])

    # Remove songs from playlist
    if len(to_delete) > 0:
        sp.playlist_remove_all_occurrences_of_items(
            playlist_id=playlist_id, items=to_delete)


# Run program
if __name__ == '__main__':
    # Loop through the list of playlist
    # Can be swapped for variables if you only have 1 playlist
    for playlist in spotify_playlists:
        spotify_spam_remover(playlist_id=playlist, allow_list=allow_list)
