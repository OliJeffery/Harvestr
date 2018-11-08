$( document ).ready(

	function() {
		data = $('#content').data();
		page_number = data.startingPageNumber;
		load_harvest(page_number, 'pitchfork');
	}
)

$(document).on("click",".nextPage",function() {
    data = $(this).data();
    load_harvest(data.pageNumber, data.scythe)
});

function load_harvest(page_number, scythe) {
	$.get( "/harvestrs/"+scythe+"/"+page_number, function( data ) {
	  $( "#content" ).fadeOut(100, function() {
	  	$( "#content" ).html( data ).fadeIn(100)
	  });
	  console.log('Page ' + page_number + ' of ' + scythe + ' loaded successfully.')
	});
}

$(document).on("click",".album",function() {
	add_album($(this), 0, 0);
});

$(document).on("click",".addToPlaylist",function() {
	$('.modal').html('<p>Commencing the harvest.</p>').fadeIn(200);
	albums = $('.album');
	number_of_albums = albums.length-1;
	console.log(number_of_albums);
	add_album(albums, 0, number_of_albums);
});

function add_album(albums, album_number, number_of_albums) {
	if (album_number<=number_of_albums) {
		if (typeof number_of_albums == 0) {
			album = albums;
		}
		else {
			album = $(albums[album_number])
		}
		if(album_number == 0) {$('.modal').data().tracksUploaded = 0;}
		data = album.data();
		$( ".modal" ).html('<p>Searching for <b>' + data.albumName +'</b> by <b>' + data.artists + '</b></p>').fadeIn(100)
	    $.get( "/album/"+data.albumName+"/"+data.artists, function( data ) {
		  $( ".modal" ).html(data);
		  var tracks = $('.track')
		  var number_of_tracks = tracks.length;
		  if(number_of_tracks == 0) {
		  	setTimeout(function(){ add_album(albums, album_number+1, number_of_albums); }, 1500);		  	
		  }
		  var i = 0;
		  tracks.each(
		  	function() {	  		
		  		var track = $(this);
		  		var track_data = track.data();
		  		var track_id = track_data.trackId;
		  		$.get( "/track/"+track_id, function(confirmation) {
		  			console.log(confirmation);	  			
		  			track.attr('style', 'background: brown');
		  			i+=1;
		  			if(i==number_of_tracks) {
		  				setTimeout(function(){ 				
		  					$('.modal').data().tracksUploaded+=i;
		  					add_album(albums, album_number+1, number_of_albums);
		  				}, 500);
		  			}
		  		});
		  	}
		  )
		});
	}
	else {
		$('.modal').text('Harvest complete. We added '+ $('.modal').data().tracksUploaded +' tracks to your HARVESTR playlist on Spotify.')
		setTimeout(function(){ 				
			$('.modal').fadeOut(2000);
		}, 3000);		
	}
}

$(document).on("click",".modal",function() {
	$(this).fadeOut(200);
});

console.log('Only sick music makes money today.')