from spotify_classes.spotify_user import SpotifyUser
from spotify_classes.spotify_search import SpotifySearch
from mysql_classes.mysql_connection import Database
from scythes.pitchfork import Pitchfork
from datetime import datetime

class HTMLPage:

	def __init__(self):
		self.user = SpotifyUser()
		self.profile = self.user.my_profile()
		self.mysql = Database().connection
		self.check_for_user(self.profile['id'])
		self.check_for_playlists(self.profile['id'])

	def check_for_user(self, spotify_id):
		sql = f"SELECT `spotify_id` FROM `users` WHERE `spotify_id` = '{spotify_id}';"
		user_check = len(self.mysql.get_rows(self.mysql.cmd_query(sql))[0])
		if user_check != 0:
			print('This user exists')
		else:
			today = datetime.today().strftime('%Y-%m-%d')
			query = "INSERT INTO `users` (`spotify_id`,`display_name`,`first_login`,`last_login`) VALUES (%s,%s,%s,%s);"
			args = [self.profile['id'],self.profile['display_name'],today,today]
			cursor = self.mysql.cursor()
			cursor.execute(query, args)
			self.mysql.commit()
			print('Added user to the MySql database')

	def check_for_playlists(self, spotify_id):
		sql = f"SELECT `main_playlist_id` FROM `users` WHERE `spotify_id` = '{spotify_id}';"
		self.playlist_id = self.mysql.get_rows(self.mysql.cmd_query(sql))[0][0][0]
		if self.playlist_id is None:
			# Playlist doesn't exist, create one.
			print('This user doesn\'t have a HARVESTR playlist set up yet.')
			self.create_list()
		else:
			# Playlist exists in MySql, try to fetch it and create a new one if not fetchable.
			"""print('Trying to fetch existing playlist.')
			current_tracks = self.user.make_request(f'playlists/{self.playlist_id}')
			print('==================================================================')
			print(current_tracks['external_urls'])
			print('==================================================================')
			"""

	def create_list(self):
		created_list = self.user.create_playlist(self.profile['id'])
		query = "UPDATE `users` SET `main_playlist_id` = %s WHERE `spotify_id` = %s; "
		args = [created_list['id'],self.profile['id']]
		cursor = self.mysql.cursor()
		cursor.execute(query, args)
		self.mysql.commit()
		self.playlist_id = created_list['id']

	def render_page(self):
		header = open('pages/static/header.html').read().format(self.profile['display_name'],self.profile['images'][0]['url'])
		footer = open('pages/static/footer.html').read()
		html = ''
		today = datetime.today().strftime('%Y-%m-%d')
		albums = self.get_albums()
		html+=self.process_albums(albums)
		return f"{header}{html}{footer}"	

	def get_albums(self):
		pitchfork = Pitchfork()
		url = pitchfork.base_url+'3'
		return(pitchfork.find_albums(url))

	def process_albums(self, albums):
		html=''
		for album in albums:
			query = album['album_name'] + ' ' + ' '.join(album['artists'])
			search = SpotifySearch(query, self.profile['id'])
			html+=f"<p>Finding <b>{album['album_name']}</b> by <b>{' & '.join(album['artists'])}</b>.</p>"
			try:
				search.add_to_playlist(self.playlist_id)
			except IndexError:
				html+=f"Hmmm, we couldn't find <b>{album['album_name']}</b> by <b>{' & '.join(album['artists'])}</b>."
		return html