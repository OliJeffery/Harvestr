from flask import make_response
from flask import request as params
from .spotify_connection import SpotifyConnection
import os

class SpotifyUser(SpotifyConnection):

	def __init__(self):
		SpotifyConnection.__init__(self)
		self.code = None
		try:
			self.token = params.cookies['access_token']
		except KeyError:
			self.require_login()

	def login(self, referrer='https://harvestr101.appspot.com/'):
		redirect_base = self.redirect_base()
		referrer = redirect_base
		scope = "user-library-read "\
		"user-library-modify "\
		"playlist-read-private "\
		"playlist-modify-public "\
		"playlist-modify-private "\
		"user-read-recently-played "\
		"user-top-read"
		body_params = {'client_id' : self.client_id, 'scope' : scope, 'response_type' : 'code', 'redirect_uri' : f'{redirect_base}/login_callback'}
		url = 'https://accounts.spotify.com/authorize/?' + self.query_string(body_params)
		response = make_response(self.redirect_to(url))
		response.set_cookie('referrer', referrer)
		return response

	def redirect_base(self):
		if os.environ.get('GAE_ENV') == 'standard':
			redirect_base = "https://harvestr101.appspot.com"
		else:
			redirect_base = "http://127.0.0.1:5000"
		return redirect_base

	def get_access_token(self, code):
		redirect_base = self.redirect_base()
		body_params = {	
						'grant_type' : 'authorization_code', 
						'code': code , 
						'redirect_uri' : f'{redirect_base}/login_callback'
					  }		
		url = 'https://accounts.spotify.com/api/token'
		return self.post_request(url, body_params)

	def refresh_access_token(self):
		redirect_base = self.redirect_base()
		body_params = {	
						'grant_type' : 'refresh_token', 
						'refresh_token': params.cookies['refresh_token'] , 
						'redirect_uri' : f'{redirect_base}/refresh_callback'
					  }		
		url = 'https://accounts.spotify.com/api/token'
		return self.post_request(url, body_params)

	def my_profile(self):
		return self.make_request('me')


	def require_login(self):
		response = make_response(self.redirect_to('/login'))
	