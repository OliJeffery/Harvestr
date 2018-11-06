from scythes.pitchfork import Pitchfork

class AlbumHarvestr:

	def __init__(self, scythe = Pitchfork()):
		self.scythe = scythe

	def harvest(self, page_number):
		html = f'<h2 class="left_floated">Page {page_number} of Pitchfork</h2>'
		html += f"""
			<div class='buttons'>
				<a class='buttony nextPage' data-page-number='{int(page_number)+1}' data-scythe='pitchfork'>More</a>
				<a class='buttony addToPlaylist' data-page-number='{page_number}' data-scythe='pitchfork'>Harvest</a>
			</div>

		"""
		self.albums = self.get_albums(page_number)
		for album in self.albums:
			html += f"""<div class='album'>
						{album['album_cover'][0]}
						<b>{album['album_name']}</b> by <b>{' & '.join(album['artists'])}</b> 
					</div>"""
		return html

	def get_albums(self, page_number):
		url = self.scythe.base_url+str(page_number)
		return(self.scythe.find_albums(url))

	def process_albums(self, albums):
		html=''
		for album in albums:
			query = album['album_name'] + ' ' + ' '.join(album['artists'])
			search = SpotifySearch(query, self.profile['id'])
			html+=f"<p>Finding <b>{album['album_name']}</b> by <b>{' & '.join(album['artists'])}</b>.</p>"
			try:
				search.add_to_playlist(self.playlist_id)
			except IndexError:
				html+=f"Hmmm, we couldn't find <b>{album['album_name']}</b> by <b>{' & '.join(album['artists'])}</b>."
		return html
