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


def parse_search_queries(results):
    search_queries = []
    for track in results:
        if track['track'] is not None:
            title = track['track']['name']
            first_artist = track['track']['artists'][0]['name']
            search_query = ';;'.join([title, first_artist])
            search_queries.append(search_query)
        else:
            print track
        # for cases of multiple artists
        # UNFORT: hurts search results when its too specific
        # artists = []
        # for artist in track['track']['artists']:
        #     artists.append(artist['name'])

    return search_queries


def get_search_queries(username, playlist_id):
    results = sp.user_playlist(username, playlist_id)
    items = results['tracks']['items']
    next_uri = results['tracks']

    playlist_title = results['name']
    if (results['tracks']['next']):
        results = sp.next(next_uri)
        more_items = results['items']
        items.extend(more_items)

    try:
        while(results['next']):
            results = sp.next(results)
            more_items = results['items']
            items.extend(more_items)
            print len(items)
    except:
        print "Failed to retrieve tracks for %s" % (playlist_title)

    search_queries = parse_search_queries(items)
    #
    return (playlist_title, search_queries)

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
