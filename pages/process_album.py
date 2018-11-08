from spotify_classes.spotify_search import SpotifySearch
from spotify_classes.spotify_user import SpotifyUser
from mysql_classes.mysql_connection import Database
from datetime import datetime
from flask import request as params
from flask import make_response
from flask import redirect

class ProcessAlbum:

	def __init__(self):
		try:
			self.user = SpotifyUser()
			self.profile = self.user.my_profile()
			self.mysql = Database().connection
			sql = f"SELECT `main_playlist_id`,`current_releases_only` FROM `users` WHERE `spotify_id` = '{self.profile['id']}';"
			user_info = self.mysql.get_rows(self.mysql.cmd_query(sql))[0]
			self.playlist_id = user_info[0][0]
			self.current_releases_only = user_info[0][1]
			self.year = datetime.today().strftime('%Y')
		except KeyError:
			self.refresh_token()

	def redirect_to(self, url):
		return redirect(url, code=302)

	def refresh_token(self):
		referrer = params.url
		print(f'Referrer is {referrer}')
		response = make_response(self.redirect_to('/refresh_token'))
		response.set_cookie('referrer', referrer)
		return response	

	def find_album(self, album_name, artists):
		query = (album_name + ' ' + artists.replace(' & ', ' ')).replace(' EP', '')
		user_id = self.profile['id']
		search = SpotifySearch(query, user_id)
		total_tracks = 0
		try:
			search.get_album_data()
			if self.current_releases_only == 1 and self.year not in search.release_date:
				html = "<p class='skip_this'>This isn't a current release, so we're skipping it.</p>"
			else:
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
		try:
			self.user.add_track(self.playlist_id, track_id)
			return f'Successfully added track {track_id}'
		except Exception as error:
			return error
