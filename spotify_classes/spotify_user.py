from flask import make_response
from flask import request as params
from .spotify_connection import SpotifyConnection

class SpotifyUser(SpotifyConnection):

	def __init__(self):
		SpotifyConnection.__init__(self)
		self.code = None
		try:
			self.token = params.cookies['access_token']
		except KeyError:
			self.require_login()

	def login(self):
		scope = "user-library-read "\
		"user-library-modify "\
		"playlist-read-private "\
		"playlist-modify-public "\
		"playlist-modify-private "\
		"user-read-recently-played "\
		"user-top-read"
		body_params = {'client_id' : self.client_id, 'scope' : scope, 'response_type' : 'code', 'redirect_uri' : 'http://127.0.0.1:5000/login_callback'}
		url = 'https://accounts.spotify.com/authorize/?' + self.query_string(body_params)
		response = make_response(self.redirect_to(url))
		return response

	def get_access_token(self, code):
		body_params = {	
						'grant_type' : 'authorization_code', 
						'code': code , 
						'redirect_uri' : 'http://127.0.0.1:5000/login_callback'
					  }		
		url = 'https://accounts.spotify.com/api/token'
		return self.post_request(url, body_params)

	def my_profile(self):
		return self.make_request('me')
