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

@APP.route('/<path:page_number>')
def specify_page(page_number):
	return pages.main_page.HTMLPage().render_page(page_number)

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

@APP.route('/album/<path:album_name>/<path:artists>')
def harvest_album(album_name, artists):
	return pages.process_album.ProcessAlbum().find_album(album_name, artists)

@APP.route('/track/<path:track_id>')
def add_track_to_playlist(track_id):
	return pages.process_album.ProcessAlbum().add_track_to_playlist(track_id)

@APP.route('/login')
def login_to_spotify():
	referrer = params.referrer 
	user = SpotifyUser()
	return user.login(referrer)

@APP.route('/login_callback')
def login_callback():
	code = params.args['code']
	user = SpotifyUser()
	token_info = user.get_access_token(code)
	access_token = token_info['access_token']
	expiration = token_info['expires_in']
	refresh_token = token_info['refresh_token']
	referrer = params.cookies['referrer']
	response = make_response(user.redirect_to(referrer))
	response.set_cookie('access_token', access_token)
	response.set_cookie('expiration', str(expiration))
	response.set_cookie('refresh_token', refresh_token)
	return response

@APP.route('/refresh_token')
def refresh_callback():
	user = SpotifyUser()
	token_info = user.refresh_access_token()
	access_token = token_info['access_token']
	expiration = token_info['expires_in']
	referrer = params.cookies['referrer']
	response = make_response(user.redirect_to(referrer))
	#response = make_response()
	response.set_cookie('access_token', access_token)
	response.set_cookie('expiration', str(expiration))
	return response
