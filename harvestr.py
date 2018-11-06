import pathlib
from flask import Flask
from flask import request as params
from flask import send_from_directory
from flask import make_response
#from spotify_classes.spotify_connection import SpotifyConnection
from spotify_classes.spotify_search import SpotifySearch
from spotify_classes.spotify_user import SpotifyUser
import pages
import requests

APP = Flask(__name__)

@APP.route('/')
def home_page():
	return pages.main_page.HTMLPage().render_page()

@APP.route('/html/<path:filename>')
def html_files(filename):
	return send_from_directory('pages/static/', filename)

@APP.route('/css/<path:filename>')
def css_files(filename):
	return send_from_directory('pages/static/', filename)

@APP.route('/js/<path:filename>')
def js_files(filename):
	return send_from_directory('pages/static/', filename)

@APP.route('/harvestrs/<path:scythe>/<path:page_number>')
def preview_albums(scythe, page_number):
	return pages.album_harvestr.AlbumHarvestr().harvest(page_number)

@APP.route('/harvestrs/<path:scythe>/<path:page_number>/harvest')
def harvest_albums(scythe, page_number):
	return pages.album_harvestr.AlbumHarvestr().harvest(page_number, True)

@APP.route('/login')
def login_to_spotify():
	user = SpotifyUser()
	return user.login()

@APP.route('/login_callback')
def login_callback():
	code = params.args['code']
	user = SpotifyUser()
	token_info = user.get_access_token(code)
	access_token = token_info['access_token']
	expiration = token_info['expires_in']
	refresh_token = token_info['refresh_token']
	#referrer = params.cookies['referrer']
	referrer = 'http://127.0.0.1:5000'
	response = make_response(user.redirect_to(referrer))
	response.set_cookie('access_token', access_token)
	response.set_cookie('expiration', str(expiration))
	response.set_cookie('refresh_token', refresh_token)
	return response