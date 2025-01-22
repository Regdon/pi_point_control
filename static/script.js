document.addEventListener('DOMContentLoaded', function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        console.log('WebSocket connected');
    });

    socket.on('update', function (msg) {
        console.log('Received message: ' + msg.points);
        
        // var c = document.getElementById("canvas");
        // var ctx = c.getContext("2d");
        // ctx.moveTo(msg.points(0).position(0).x, msg.points(0).position(0).y);
        // ctx.lineTo(msg.points(0).position(1).x, msg.points(0).position(1).y);
        
        // ctx.moveTo(msg.points(0).position(0).x, msg.points(0).position(0).y);
        // ctx.lineTo(msg.points(0).position(2).x, msg.points(0).position(2).y);
        // ctx.stroke();

    });
});






// <script>
// var c = document.getElementById("myCanvas");
// var ctx = c.getContext("2d");
// ctx.moveTo(0, 0);
// ctx.lineTo(200, 100);
// ctx.stroke();
// </script>