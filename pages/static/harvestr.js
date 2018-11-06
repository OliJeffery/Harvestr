$( document ).ready(

	load_harvest(1, 'pitchfork')

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



console.log('Only sick music makes money today.')