from flask import request as params
from .spotify_connection import SpotifyConnection
from mysql_classes.mysql_connection import Database
from datetime import datetime

class SpotifySearch(SpotifyConnection):

	def __init__(self, query, user_id):
		SpotifyConnection.__init__(self)
		self.code = None
		self.user_id = user_id
		try:
			self.token = params.cookies['access_token']
			self.mysql = Database().connection
			self.search(query)
		except KeyError:
			self.require_login()

	def search(self, query, limit='1', search_type='album', market='GB'):
		payload = {'q':query, 'type':search_type, 'limit':limit, 'market':market}
		self.results = self.make_request('search', payload)

	def add_to_playlist(self, playlist_id):
		tracks = self.get_tracks()
		add_tracks = self.add_tracks(playlist_id, tracks)
		#print(add_tracks)

	def get_tracks(self):
		#print(self.results)
		album_id = self.results['albums']['items'][0]['id']
		tracks = self.make_request(request=f'albums/{album_id}/tracks',params={"limit":50})
		uris = []
		for track in tracks['items']:
			sql = f"SELECT `track_id` FROM `processed_tracks` WHERE `spotify_id` = '{self.user_id}' AND `track_id` = '{track['id']}';"
			already_processed = len(self.mysql.get_rows(self.mysql.cmd_query(sql))[0])
			if already_processed == 0:
				query = 'INSERT INTO `processed_tracks` (`spotify_id`,`track_id`,`processed`) VALUES(%s,%s,%s);'
				args = [self.user_id, track['id'], datetime.today().strftime('%Y-%m-%d %H:%M:%S')]
				cursor = self.mysql.cursor()
				cursor.execute(query, args)
				self.mysql.commit()
				uris.append(f"spotify:track:{track['id']}")
		return uris
	