$(function () {
	socket = io.connect('http://' + document.domain + ':' + location.port);
	socket.on('connect', function() {
		$('#status').text('Connecté');
    	socket.emit('client_connected', {data: 'New client!'});
	});

	socket.on('disconnect', function() {
		$('#status').text('Déconnecté');
	});

        socket.on('alert', function (data) {
                $('#content').text(data);
                $('body').toggleClass('stop-cat');
                $('.btn-distract').attr('aria-disabled', 'false');
		$('.btn-distract').toggleClass('disabled');
        });        


});

