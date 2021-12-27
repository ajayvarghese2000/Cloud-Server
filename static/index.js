
// Create SocketIO instance, connect

var socket = new io('http://ajayvarghese.me', {
  path: "/ws/socket.io/"
});

function getnewframe(socket) {
  socket.emit('getframe', "hi")
}

setInterval(getnewframe,10,socket)

// Add a connect listener
socket.on('connect',function() {
  console.log('Client has connected to the server!');
});
// Add a connect listener
socket.on('BASE64SEND',function(data) {
  var c = document.getElementById("myCanvas");
  var ctx = c.getContext("2d");
  var img = new Image()
  
  img.onload = function() {
    ctx.drawImage(img, 0, 0);
  };

  img.src = 'data:image/png;base64,' + data
  //console.log('Received a message from the server!');
});
// Add a disconnect listener
socket.on('disconnect',function(sid) {
  console.log('The client has disconnected! ' + sid);
});


/*
function myCanvas() {
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    var img = new Image()
    img.src = 1;
    ctx.drawImage(img,0,0);
  }*/
