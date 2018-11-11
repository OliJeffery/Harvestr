from spotify_classes.spotify_user import SpotifyUser
from mysql_classes.pymysql_connection import Database
from datetime import datetime

class HTMLPage:

	def __init__(self):
		self.user = SpotifyUser()
		try:
			self.profile = self.user.my_profile()
			#self.mysql = Database().connection
			self.check_for_user(self.profile['id'])
			self.check_for_playlists()
			self.logged_in = True
		except KeyError:
			self.logged_in = False

	def check_for_user(self, spotify_id):
		sql = f"SELECT `spotify_id` FROM `users` WHERE `spotify_id` = '{spotify_id}';"
		try:
			user_check = len(Database().query(sql))
		except:
			return str(Database().query(sql))
		if user_check != 0:
			print('This user exists')
		else:
			today = datetime.today().strftime('%Y-%m-%d')
			query = "INSERT INTO `users` (`spotify_id`,`display_name`,`first_login`,`last_login`) VALUES (%s,%s,%s,%s);"
			args = [self.profile['id'],self.profile['display_name'],today,today]
			Database().update(query, args)
			print('Added user to the MySql database')

	def check_for_playlists(self):
		spotify_id = self.profile['id']
		sql = f"SELECT `main_playlist_id` FROM `users` WHERE `spotify_id` = '{spotify_id}';"
		playlist_check = Database().query(sql)
		self.playlist_id = playlist_check[0]['main_playlist_id']
		if self.playlist_id is None:
			# Playlist doesn't exist, create one.
			print('This user doesn\'t have a HARVESTR playlist set up yet.')
			self.create_list()
		else:
			print(f'PLAYLIST ID: {self.playlist_id}')
		
	def create_list(self):
		created_list = self.user.create_playlist(self.profile['id'])
		query = "UPDATE `users` SET `main_playlist_id` = %s WHERE `spotify_id` = %s; "
		args = [created_list['id'],self.profile['id']]
		Database().update(query, args)
		self.playlist_id = created_list['id']
		print(f'CREATED NEW PLAYLIST: {self.playlist_id}')

	def render_page(self, page_number=1):
		if self.logged_in:
			header = open('pages/static/header.html').read()
			try:
				profile_image = self.profile['images'][0]['url']
			except IndexError:
				profile_image = '/img/generic_profile.jpg'
			profile_pic = """
							<div class='profile'>
		  						<img class='profile_pic' alt='{}' src='{}' />
		  					</div>
		  				  """.format(self.profile['display_name'],profile_image)
			footer = open('pages/static/footer.html').read()
			html = f"""
				{profile_pic}
				<section id="content" data-starting-page-number="{page_number}">
					<h2>Fetching latest reviews from Pitchfork.</h2>
				</section>
			"""
			today = datetime.today().strftime('%Y-%m-%d')
			return f"{header}{html}{footer}"	
		else:
			header = open('pages/static/header.html').read()
			footer = open('pages/static/footer.html').read()
			html = "<a href='/login' class='buttony login'>Log in via Spotify</a>"	
			return f"{header}{html}{footer}"