import requests
import sys
from bs4 import BeautifulSoup
from string import punctuation

# CRIBBD: https://stackoverflow.com/questions/4906977/access-environment-variables-from-python
# securing environment variables

base_url = "http://api.genius.com"
bearer_token = 'Bearer %s ' % (os.environ['GENIUS_TOKEN'])
headers = {'Authorization': bearer_token}

def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    #gotta go regular html scraping... come on Genius
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    #remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]
    #at least Genius is nice and has a tag called 'lyrics'!
    lyrics = html.find("div", class_="lyrics").get_text() #updated css where the lyrics are based in HTML
    return lyrics

# CRIBBD: https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/
if __name__ == "__main__":
    song_title = sys.argv[1]
    artist_name = sys.argv[2]

    search_url = base_url + "/search"
    data = {'q': song_title}
    response = requests.get(search_url, params=data, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"].lower() == artist_name.lower():
            song_info = hit
            break
    if song_info:
        song_api_path = song_info["result"]["api_path"]
        lyrics = lyrics_from_song_api_path(song_api_path)
        output_file_name = "".join((char for char in song_title if char not in punctuation)).replace(" ", "_").lower() + '.txt'
        text_file = open('lyrics/' + output_file_name, "w")
        for line in lyrics.splitlines():
            text_file.write(line.encode('utf8') + '\n')
        text_file.close()
