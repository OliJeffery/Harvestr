""" Connect to Spotify API """

import json
import base64
from urllib import parse
import requests
from flask import Flask,redirect
import json

class SpotifyConnection:

	def __init__(self):
		with open('../spotify_credentials.json') as credentials:
			json_credentials = json.loads(credentials.read())
			#self.auth = str(base64.b64encode(bytes(json_credentials['client_id']+':'+json_credentials['client_secret'], 'utf-8'))).split("'")[1]
			self.client_id = json_credentials['client_id']
			self.client_secret = json_credentials['client_secret']
			self.accounts_url = 'https://accounts.spotify.com/api/'
			self.base_url = 'https://api.spotify.com/v1/'
			self.token = self.get_token()

	def get_token(self):
		body_params = {'grant_type' : 'client_credentials'}
		url = self.accounts_url+'token'
		response=requests.post(url, data=body_params, auth = (self.client_id, self.client_secret))
		return response.json()['access_token']

	def make_request(self, request, params=None):
		url = self.base_url+request
		headers = {'Authorization':f'Bearer {self.token}'}
		response = requests.get(url,headers=headers,params=params)
		return response.json()

	def redirect_to(self, url):
		return redirect(url, code=302)

	def query_string(self, string):
		return parse.urlencode(string)

	def post_request(self, url, body_params):
		response=requests.post(url, data=body_params, auth = (self.client_id, self.client_secret))
		return response.json()

	def create_playlist(self, user_id, playlist_name='HARVESTR', playlist_description='Created by HARVESTR, getting albums reviewed from Pitchfork.'):
		request = f"users/{user_id}/playlists"
		url = self.base_url+request
		headers = {'Authorization':f'Bearer {self.token}'}
		payload = f'{{"name": "{playlist_name}", "description": "{playlist_description}"}}'
		response = requests.post(url,headers=headers,data=payload)
		return response.json()

	def add_tracks(self, playlist_id, tracks):
		request = f"playlists/{playlist_id}/tracks"
		url = self.base_url+request
		headers = {'Authorization':f'Bearer {self.token}','Content-Type':'application/json'}
		payload = '{"uris": ["'+'","'.join(tracks)+'"]}'
		response = requests.post(url,headers=headers,data=payload)
