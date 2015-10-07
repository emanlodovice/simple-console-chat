$('#connect-form').on('submit', function(e) {
    e.preventDefault();
    var form = $(this);
    var url = form.find('#url').val();
    if (url) {
        connect(url);
        $('#thread').empty();
    }
});

$('#message-form').on('submit', function(e) {
    e.preventDefault();
    var form = $(this);
    var textarea = form.find('textarea');
    var message = textarea.val();
    textarea.val('');
    if (message && socket != null) {
        var msg = {'username': userInfo.username, 'message': message}
        socket.send(JSON.stringify(msg));
        textarea.focus();
    }
});

var socket = null;
var userInfo = {'username': 'default'};

function connect(url) {
    socket = new WebSocket(url);
    attachSocketListeners();
}

function attachSocketListeners() {
    socket.onopen = sendUserInfo;
    socket.onmessage = handleMessage;
}

function sendUserInfo(e) {
    var username = 'default';
    username = $('#username').val();
    userInfo = {'username': username};
    var msg = {'username': username, 'message': 'hello'}
    socket.send(JSON.stringify(msg));
}

function handleMessage(e) {
    var data = e.data;
    $('#thread').append('<li>' + data + '</li>');
}