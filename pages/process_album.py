from spotify_classes.spotify_search import SpotifySearch
from spotify_classes.spotify_user import SpotifyUser
from mysql_classes.mysql_connection import Database
from datetime import datetime

class ProcessAlbum:

	def __init__(self):
		self.user = SpotifyUser()
		self.profile = self.user.my_profile()
		self.mysql = Database().connection
		sql = f"SELECT `main_playlist_id` FROM `users` WHERE `spotify_id` = '{self.profile['id']}';"
		self.playlist_id = self.mysql.get_rows(self.mysql.cmd_query(sql))[0][0][0]
		
	#def start_search(self, album_name, artists):
	#	html=''
	#	query = album_name + ' ' + artists
	#	search = SpotifySearch(query, self.profile['id'])
	#	html+=f"<p>Searching for <b>{album_name}</b> by <b>{artists}</b> on Spotify.</p>"
	#	return html

	def find_album(self, album_name, artists):
		query = album_name + ' ' + artists.replace(' & ', ' ')
		user_id = self.profile['id']
		search = SpotifySearch(query, user_id)
		total_tracks = 0
		try:
			search.get_album_data()
			already_processed = search.check_if_processed()
			if already_processed == 0:
				album_id = search.album_id			
				total_tracks = search.total_tracks
				if(total_tracks>50):
					total_tracks = 50
				html=f"<p class='harvesting' data-album-id='{album_id}'>Album found. Harvesting {total_tracks} tracks.</p><ul class='tracks'>"
				for track in search.tracks:
					html+=f"<li class='track' data-track-id='{track['id']}'>{track['name']}</li>"
				html+='</ul>'
			else:
				html = "<p class='skip_this'>You've already added this album to your HARVESTR playlist, so we're gonna skip it.</p>"
		except IndexError:
			html=f"<p class='skip_this'>Hmmm, we couldn't find <b>{album_name}</b> by <b>{artists}</b> on Spotify. Sorry!</p>"
		return html

	def add_track_to_playlist(self, track_id):
		self.user.add_track(self.playlist_id, track_id)
		return f'Successfully added track {track_id}'
