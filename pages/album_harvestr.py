from scythes.pitchfork import Pitchfork
from spotify_classes.spotify_search import SpotifySearch
from spotify_classes.spotify_user import SpotifyUser
from mysql_classes.mysql_connection import Database
from datetime import datetime

class AlbumHarvestr:

	def __init__(self, scythe = Pitchfork()):
		self.scythe = scythe

	def harvest(self, page_number, harvest=False):
		self.albums = self.get_albums(page_number)
		if harvest:
			return self.process_albums()
		else:
			html = f'<h2 class="left_floated">Page {page_number} of Pitchfork</h2>'
			html += f"""
				<div class='buttons'>
					<a class='buttony nextPage' data-page-number='{int(page_number)+1}' data-scythe='pitchfork'>More</a>
					<a class='buttony addToPlaylist' data-page-number='{page_number}' data-scythe='pitchfork'>Harvest</a>
				</div>

			"""			
			for album in self.albums:
				html += f"""<div class='album'>
							{album['album_cover'][0]}
							<b>{album['album_name']}</b> by <b>{' & '.join(album['artists'])}</b> 
						</div>"""
			return html

	def get_albums(self, page_number):
		url = self.scythe.base_url+str(page_number)
		return(self.scythe.find_albums(url))

	def process_albums(self):
		self.user = SpotifyUser()
		self.profile = self.user.my_profile()
		self.mysql = Database().connection
		sql = f"SELECT `main_playlist_id` FROM `users` WHERE `spotify_id` = '{self.profile['id']}';"
		self.playlist_id = self.mysql.get_rows(self.mysql.cmd_query(sql))[0][0][0]
		html=''
		for album in self.albums:
			query = album['album_name'] + ' ' + ' '.join(album['artists'])
			search = SpotifySearch(query, self.profile['id'])
			html+=f"<p>Harvesting <b>{album['album_name']}</b> by <b>{' & '.join(album['artists'])}</b>.</p>"
			try:
				search.add_to_playlist(self.playlist_id)
			except IndexError:
				html+=f"Hmmm, we couldn't find <b>{album['album_name']}</b> by <b>{' & '.join(album['artists'])}</b>."
		return html
