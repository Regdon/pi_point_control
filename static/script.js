function drawLine(ctx, x1, y1, x2, y2, colour) {
    ctx.strokeStyle = colour;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    ctx.closePath();
};

document.addEventListener('DOMContentLoaded', function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        console.log('WebSocket connected');
    });

    socket.on('update', function (msg) {
        console.log('Received message: ' + msg);
        let msgObject = JSON.parse(msg);

        var c = document.getElementById("canvas");
        var ctx = c.getContext("2d");
        
        msgObject.forEach((i) => {
            drawLine(ctx, i.x1, i.y1, i.x2, i.y2, i.state);
        });
    });
});






// <script>
// var c = document.getElementById("myCanvas");
// var ctx = c.getContext("2d");
// ctx.moveTo(0, 0);
// ctx.lineTo(200, 100);
// ctx.stroke();
// </script>