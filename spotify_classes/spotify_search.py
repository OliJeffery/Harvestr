from flask import request as params
from .spotify_connection import SpotifyConnection
from mysql_classes.mysql_connection import Database
from datetime import datetime

class SpotifySearch(SpotifyConnection):

	def __init__(self, query, user_id):
		SpotifyConnection.__init__(self)
		self.code = None
		self.user_id = user_id
		self.token = params.cookies['access_token']
		self.mysql = Database().connection
		self.search(query)
		
	def search(self, query, limit='1', search_type='album', market='GB'):
		payload = {'q':query, 'type':search_type, 'limit':limit, 'market':market}
		self.results = self.make_request('search', payload)

	def get_album_data(self):
		album = self.results['albums']['items'][0]
		self.album_id = album['id']
		self.release_date = album['release_date']
		self.total_tracks = album['total_tracks']
		self.tracks = self.make_request(request=f'albums/{self.album_id}/tracks',params={"limit":50})['items']

	def check_if_processed(self):
		sql = f"SELECT `album_id` FROM `processed_albums` WHERE `spotify_id` = '{self.user_id}' AND `album_id` = '{self.album_id}';"
		already_processed = len(self.mysql.get_rows(self.mysql.cmd_query(sql))[0])
		if already_processed == 0:
			query = 'INSERT INTO `processed_albums` (`spotify_id`,`album_id`,`processed`) VALUES(%s,%s,%s);'
			args = [self.user_id, self.album_id, datetime.today().strftime('%Y-%m-%d %H:%M:%S')]
			cursor = self.mysql.cursor()
			cursor.execute(query, args)
			self.mysql.commit()
		return already_processed
		