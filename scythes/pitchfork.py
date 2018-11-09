import requests
from bs4 import BeautifulSoup

class Pitchfork:

	def __init__(self):
		self.base_url = 'https://pitchfork.com/reviews/albums/?page='
		self.albums = None

	def find_albums(self, url):
		response = requests.get(url)
		if response.status_code == 200:
			html = BeautifulSoup(response.text, 'html.parser')
			self.albums = html.select('.review')
			processed_albums = self.process_albums()
			return processed_albums
		else:
			return("Couldn't connect to that page.")

	def process_albums(self):
		returned_albums = []
		for album in self.albums:
			spotify_info = {
				"album_name":None,
				"artists":[]
			}
			artists = album.select('.review__title-artist li')
			for artist in artists:
				spotify_info['artists'].append(artist.get_text())
			spotify_info['album_name'] = album.select('.review__title-album')[0].get_text()
			spotify_info['album_cover'] = album.select('.review__artwork img')
			returned_albums.append(spotify_info)
		return returned_albums
