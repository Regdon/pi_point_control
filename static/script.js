function drawLine(ctx, x1, y1, x2, y2, colour) {
    ctx.strokeStyle = colour;
    ctx.lineWidth = 5;
    ctx.lineCap = "round";

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

const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

canvas.addEventListener('click', function(event) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    console.log('Click coordinates: (' + x + ', ' + y + ')');
});
