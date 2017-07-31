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
        search_query = ';;'.join([title, first_artist])
        search_queries.append(search_query)

    return search_queries


def get_search_queries(username, playlist_id):
    results = sp.user_playlist(username, playlist_id)
    items = results['tracks']['items']
    playlist_title = results['name']
    while(results['tracks']['next']):
        print 'getting more...'
        results = sp.next(results['tracks'])
        more_items = results['items']
        items.append(more_items)
    print items

    # search_queries = parse_search_queries(items)
    #
    # return (playlist_title, search_queries)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    else:
        print("Usage: %s uri" % (sys.argv[0],))
        sys.exit()

    # TODO: how to handle cases of private playlists
    # TODO: user client authentication

    username, playlist_id = get_playlist_uri(uri)
    print get_search_queries(username, playlist_id)
