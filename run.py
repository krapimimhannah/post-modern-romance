import scrape
import get_playlist_tracks
import re
import sys
import os

# just a test script

if __name__ == '__main__':
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    else:
        print("Usage: %s uri" % (sys.argv[0],))
        sys.exit()

    username, playlist_id = get_playlist_tracks.get_playlist_uri(uri)

    playlist_title, search_queries = get_playlist_tracks.get_search_queries(username, playlist_id)

    for query in search_queries:
        song_title, artist_name = query.split(';;')

        # make playlist only alphanumeric characters
        pattern = re.compile('[\W_]+')
        playlist_title = pattern.sub('_', playlist_title)
        directory = 'data/' + playlist_title

        # check that the director exists already
        if not os.path.exists(directory):
            os.mkdir(directory)

        scrape.run_search(directory, song_title, artist_name)
        # PERCOLATE: passing in playlist_title at a different point
