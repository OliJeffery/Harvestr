import requests
from bs4 import BeautifulSoup

class TheQuietus:

	def __init__(self):
		self.base_url = 'https://thequietus.com/reviews?page='
		self.albums = None

	def find_albums(self, url):
		response = requests.get(url)
		if response.status_code == 200:
			html = BeautifulSoup(response.text, 'html.parser')
			self.big_reviews = html.select('.review')
			self.small_reviews = html.select('.review_small')
			processed_albums = self.process_albums()
			return processed_albums
		else:
			return("Couldn't connect to that page.")

	def process_albums(self):
		returned_albums = []
		for album in self.big_reviews:
			spotify_info = {
				"album_name":None,
				"artists":[]
			}
			review_info = str(album.select('h4')[0]).replace('<h4>','').replace('</h4>','').replace('<span class="sub">','').replace('</span>','').split('<br/>')
			artists = review_info[0].split(' & ')
			for artist in artists:
				spotify_info['artists'].append(artist)
			spotify_info['album_name'] = review_info[1]
			spotify_info['album_cover'] = album.select('img')[0]
			returned_albums.append(spotify_info)
		for album in self.small_reviews:
			spotify_info = {
				"album_name":None,
				"artists":[]
			}
			spotify_info['album_name'] = album.select('h4')[0].getText()
			artists = album.select('.sub')[0].getText().split(' & ')
			for artist in artists:
				spotify_info['artists'].append(artist)
			spotify_info['album_cover'] = album.select('img')[0]
			returned_albums.append(spotify_info)		
		return returned_albums

if __name__ == '__main__':
	scythe = TheQuietus()
	url = scythe.base_url + '1'
	print(scythe.find_albums(url))