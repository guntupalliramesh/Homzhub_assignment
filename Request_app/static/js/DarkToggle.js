$(document).ready(function(){
    $('.sidenav').sidenav();

	$('.dark-toggle').on('click',function(){
		if ($(this).find('i').text() == 'brightness_4'){
				$(this).find('i').text('brightness_high');
		} else {
				$(this).find('i').text('brightness_4');
		}
	});


});