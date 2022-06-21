from lyricsgenius import Genius
from datetime import date
from pathlib import Path
import urllib.request
import json
import time
import sys
import os

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
    print(f'\n\nFetching page {page} out of {pages}:\n')
    url = f'http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={username}&api_key={LastFmKey}&format=json&limit={perPage}&page={page}'
    songs = json.loads(urllib.request.urlopen(url).read().decode())['lovedtracks']['track']

    for i in range(len(songs)):
        songName = songs[i]['name']
        artistName = songs[i]['artist']['name']

        for c in '<>:"/\|?*':
            artistName = artistName.replace(c, '')
            songName = songName.replace(c, '')
        for word in ['(', 'feat.']:
            songName = songName.split(word, 1)[0]
        for word in ['Live', 'live', 'Remastered', 'remastered', 'Remaster', 'remaster', 'Acoustic', 'acoustic', 'EP Version', 'Single Version', 'EP version', 'single version', 'Remix', 'remix', 'Radio Edit', 'Radio Session', 'Radio Mix', 'Unpeeled', 'Bonus Track', 'bonus track', 'MTV', 'Unplugged', 'Stripped', 'mtv', 'unplugged', 'stripped', 'Recorded', 'recorded', 'Piano Version', 'Demo']:
            songName = songName.split(f'- {word}', 1)[0]
        for word in ['Remastered', 'remastered', 'Remaster', 'remaster', 'Acoustic', 'acoustic', 'EP Version', 'Single Version', 'EP version', 'single version', 'Remix', 'remix', 'Radio Edit', 'Radio Session', 'Radio Mix', 'Bonus Track', 'bonus track', '()']:
            songName = songName.replace(word, '')
        for year in range(1990, date.today().year):
            for word in [f'- {year} Digital', f'- {year}', f'({year})', f'({year} )']:
                songName = songName.replace(word, '')

        artistName = ' '.join(artistName.split())
        songName = ' '.join(songName.split())
        songName = songName.replace('( )', '')
        artistName = artistName.strip('- ')
        songName = songName.strip('- ')

        print(f'{str(i + 1).rjust(3)}/{str(len(songs)).ljust(10)} {songName.ljust(80)} {artistName}')
        filePath = Path(f'arhiva/{songName} ♢ {artistName}.txt')

        if not filePath.exists(): # or os.path.getsize(filePath) > 10000:
            file = open(filePath, 'w', encoding='utf-8')

            while True:
                try:
                    song = genius.search_song(songName, artistName)
                    break
                except:
                    print('               Exception occured! Trying again in 5 seconds...', end='\r')
                    time.sleep(5)
                    sys.stdout.write('\033[K')

            file.write(song.lyrics.replace('[', '\n\n[', 1).replace(' Lyrics', '', 1) if song is not None else '')
