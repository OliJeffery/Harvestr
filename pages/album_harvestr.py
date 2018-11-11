from scythes.pitchfork import Pitchfork

class AlbumHarvestr:

	def __init__(self, scythe = Pitchfork()):
		self.scythe = scythe

	def harvest(self, page_number, harvest=False):
		self.albums = self.get_albums(page_number)
		if harvest:
			return self.process_albums()
		else:
			html = f"""
				<div class="fixed_buttons">
					<h2 class="left_floated">Page {page_number} of Pitchfork</h2>
					<div class='buttons'>
						<a class='buttony nextPage' data-page-number='{int(page_number)+1}' data-scythe='pitchfork'>More</a>
						<a class='buttony addToPlaylist' data-page-number='{page_number}' data-scythe='pitchfork'>Harvest All</a>
					</div>
				</div>
			"""			
			for album in self.albums:
				html += f"""<div class='album' data-album-name='{album['album_name']}' data-artists='{' & '.join(album['artists'])}' >
							{album['album_cover'][0]}
							<b>{album['album_name']}</b> by <b>{' & '.join(album['artists'])}</b> 
						</div>"""
			return html

	def get_albums(self, page_number):
		url = self.scythe.base_url+str(page_number)
		return(self.scythe.find_albums(url))
		