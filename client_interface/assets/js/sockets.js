$('#connect-form').on('submit', function(e) {
    e.preventDefault();
    var form = $(this);
    var url = form.find('#url').val();
    if (url) {
        connect(url);
    }
});

var socket = null;

function connect(url) {
    socket = new WebSocket(url);
    console.log(socket);
}