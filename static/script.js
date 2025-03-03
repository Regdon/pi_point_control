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

function drawRect(ctx, x1, y1, width, height, colour) {
    ctx.fillStyle = colour;
    ctx.fillRect(x1, y1, width, height);
}

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

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        msgObject.forEach((i) => {
            if ("type" in i) {
                if (i.type == "route_button") {
                    drawRect(ctx, i.x1, i.y1, i.width, i.height, i.colour);
                }
            } else {
                drawLine(ctx, i.x1, i.y1, i.x2, i.y2, i.state);
            }
        });
    });

    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    
    canvas.addEventListener('click', function(event) {
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        console.log('Click coordinates: (' + x + ', ' + y + ')');
        socket.emit('click', {'x' : x, 'y' : y});
    });
});


// // Select the canvas element
// var canvas = document.getElementById('myCanvas');
// var ctx = canvas.getContext('2d');

// // Create an image element
// var img = new Image();

// // When the image is loaded, draw it onto the canvas
// img.onload = function() {
//     ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
// };

// // Set the source of the image (update this with your JPEG path)
// img.src = 'path/to/your/image.jpg';






// // Select the canvas element
// var canvas = document.getElementById('myCanvas');
// var ctx = canvas.getContext('2d');

// // Create an image element
// var img = new Image();

// // When the image is loaded, manipulate and draw it onto the canvas
// img.onload = function() {
//     // Draw the image onto the canvas
//     ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

//     // Get the image data
//     var imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
//     var data = imageData.data;

//     // Loop through each pixel and modify the RGB values
//     for (var i = 0; i < data.length; i += 4) {
//         // Red component
//         data[i] = data[i] * 1.2;     // Increase the red component by 20%

//         // Green component
//         data[i + 1] = data[i + 1] * 0.8; // Decrease the green component by 20%

//         // Blue component
//         data[i + 2] = data[i + 2] * 1.5; // Increase the blue component by 50%
//     }

//     // Put the modified image data back onto the canvas
//     ctx.putImageData(imageData, 0, 0);
// };

// // Set the source of the image (update this with your JPEG path)
// img.src = 'path/to/your/image.jpg';
