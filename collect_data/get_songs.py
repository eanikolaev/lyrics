"""
	get songs using VK API

	1) search songs by russian words list
        2) filter songs with text
        3) save them in OUTPUT
"""


import requests
import datetime
import csv
from wordlist import wordlist

# set your token and id here
TOKEN  = ""
ID     = ""
OUTPUT = "songs.csv"


class Api(object):

    endpoint = ''

    def __init__(self, access_token):
        self.access_token = access_token

    def call(self, method, **params):
        request_params = params.copy()
        request_params["access_token"] = self.access_token
        try:
            response = requests.get(self.endpoint.format(method=method), params=request_params)
            if response.status_code != 200:
                raise requests.exceptions.RequestException("Bad status code {}".format(response.status_code))
            return response.json()
        except requests.exceptions.RequestException as re:
            print "A n API call failed with exception {}".format(re)
            raise


class Song(object):

    def __init__(self, aid, artist, title, duration, url):
        self.aid = aid
        self.artist   = artist.encode('utf-8')
        self.title    = title.encode('utf-8')
        self.duration = duration
        self.url      = url

    def to_csv(self):
        return [ self.aid, self.artist, self.title, self.duration, self.url ]

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"Song('{aid}', '{artist}', '{title}', '{duration}', '{url}')".format(aid=self.aid, artist=self.artist, title=self.title, duration=self.duration, url=self.url)


class VkApi(Api):
    endpoint = "https://api.vk.com/method/{method}"

    def search_songs(self, query):
        json = self.call("audio.search", query=query, lyrics='1', count='200', fields="aid,artist,title,duration,url")
        for song_json in json.get("response", ["0",])[1:]:
            yield self.json_to_song(song_json)

    @staticmethod
    def json_to_song(json):
        s = Song(json['aid'], json['artist'], json['title'], json['duration'], json['url'])
        return s


def main():    
    api = VkApi(TOKEN)
    csvfile = open(OUTPUT, 'wb')
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    song_ids = set()

    for word in wordlist[10:20]:
        songs = api.search_songs(word)
        for song in songs:
            if not song.aid in song_ids:
                song_ids.add(song.aid)
                writer.writerow( song.to_csv() )


if __name__ == "__main__":
    main()
