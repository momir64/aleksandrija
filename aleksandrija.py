from lyricsgenius import Genius
import urllib.request
import json
import time
import sys

perPage = 200
username = 'momir64'
LastFmKey = '73e31e83d6b10ec1256869581540cc3c'
GeniusKey = '2WmpJsTgoFNdZxZTmNWz0p_6eIx3H8Z_229qPNUzboE1hx0sfWp3fZ0c-vP5Lshc'

url = f'http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={username}&api_key={LastFmKey}&format=json&limit={perPage}'
pages = int(json.loads(urllib.request.urlopen(url).read().decode())['lovedtracks']['@attr']['totalPages'])
totalSongs = json.loads(urllib.request.urlopen(url).read().decode())['lovedtracks']['@attr']['total']
genius = Genius(GeniusKey)
genius.verbose = False


print(f'Total number of pages: {pages}')
print(f'Total number of tracks: {totalSongs}')
print()

for page in range(1, pages + 1):
    print()
    print(f'Fetching page: {page}')
    url = f'http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={username}&api_key={LastFmKey}&format=json&limit={perPage}&page={page}'
    songs = json.loads(urllib.request.urlopen(url).read().decode())['lovedtracks']['track']

    for i in range(len(songs)):
        songName = songs[i]["name"]
        artistName = songs[i]["artist"]["name"]

        for c in '<>:"/\|?*':
            songName = songName.replace(c, '')
            artistName = artistName.replace(c, '')

        print(f'{str(i + 1).rjust(3)}/{str(len(songs)).ljust(10)} {songName.ljust(50)} {artistName}')
        f = open(f'arhiva/{songName} - {artistName}.txt', 'w', encoding='utf-8')

        while True:
            try:
                song = genius.search_song(songName, artistName)
                break
            except:
                print("               Exception occured! Trying again in 10 seconds...", end='\r')
                time.sleep(10)
                sys.stdout.write('\033[K')

        f.write(song.lyrics.replace('[', '\n\n[', 1) if song is not None else '')
