from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json

import sys
import pprint

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# parse a playlist URI when clicking 'share' on spotify application
# bless for fixed URL structure
def get_playlist_uri(uri):
    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]
    return (username, playlist_id)

# get all the tracks for that particular user
def parse_search_queries(results):
    tracks = results['tracks']['items']

    search_queries = []
    for track in tracks:
        # get the title of the track
        title = track['track']['name']

        # for cases of multiple artists
        # UNFORT: hurts search results when its too specific
        # artists = []
        # for artist in track['track']['artists']:
        #     artists.append(artist['name'])

        first_artist = track['track']['artists'][0]['name']
        search_query = ' '.join([title, first_artist])
        search_queries.append(search_query)

    return search_queries

if __name__ == '__main__':
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    else:
        print("Usage: %s uri" % (sys.argv[0],))
        sys.exit()

    username, playlist_id = get_playlist_uri(uri)
    results = sp.user_playlist(username, playlist_id)

    search_queries = parse_search_queries(results)
