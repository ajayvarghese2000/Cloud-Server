
// Create SocketIO instance, connect
var URL = window.location.protocol + "//" + window.location.host;

var socket = new io(URL, {
  path: "/ws/socket.io/"
});

/*
function getnewframe(socket) {
  socket.emit('getframe', "hi")
}

setInterval(getnewframe,10,socket)
*/

// Add a connect listener
socket.on('connect',function() {
  console.log('Client has connected to the server!');
});

var drone = "0"

// Add a connect listener
socket.on(drone,function(data) {

  var c = document.getElementById("myCanvas");
  var ctx = c.getContext("2d");
  var img = new Image()
  
  img.onload = function() {
    ctx.drawImage(img, 0, 0);
  };
  

  img.src = 'data:image/png;base64,' + data["cam"]


  //console.log(data);
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
