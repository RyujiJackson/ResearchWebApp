//script to handle drawing area of H.Pylori Infection
var canvas = document.getElementById("myCanvas");
var c  = canvas.getContext("2d");
var undoButton = document.getElementById("undo")
var mouse_on_canvas = {x:0, y:0};
var temp = 0;
const coordinates = [];
var prevent = false


canvas.addEventListener('click', onClick);
canvas.addEventListener('contextmenu', rightClick);
undoButton.addEventListener('click', undoClick);

function onClick(event) {
    if(!prevent){
        var rect = canvas.getBoundingClientRect();
        var scaleX = canvas.width / rect.width;
        var scaleY = canvas.height / rect.height;
        mouse_on_canvas.x = (event.clientX - rect.left) * scaleX;
        mouse_on_canvas.y = (event.clientY - rect.top) * scaleY;
        if(((event.clientX >= rect.left) && (event.clientY >= rect.top)))
        {
            if(((event.clientX <= rect.right)  && (event.clientY <= rect.bottom)))
            {
                temp = temp + 1
                draw()
                coordinates.push({ x: mouse_on_canvas.x, y: mouse_on_canvas.y });
            }
        }

    }
}

function rightClick(event) {
    event.preventDefault();
    if (coordinates.length > 2) {
        prevent=true

        var rect = canvas.getBoundingClientRect();
        var scaleX = canvas.width / rect.width;
        var scaleY = canvas.height / rect.height;
        mouse_on_canvas.x = (event.clientX - rect.left) * scaleX;
        mouse_on_canvas.y = (event.clientY - rect.top) * scaleY;
        if(((event.clientX >= rect.left) && (event.clientY >= rect.top)))
        {
            if(((event.clientX <= rect.right)  && (event.clientY <= rect.bottom)))
            {
                draw_polygon()
            }
        }
    }
    
}

function undoClick(event) {
    if (coordinates.length > 0) {
        temp--;
        coordinates.pop(); // Remove the last point from the coordinates array
        c.reset(); // context reset
        prevent = false; // to handle when undo right click
        draw(); // Redraw the canvas without the removed point
    }
}

function draw() {
    var lastpoint_x = 10000;
    var lastpoint_y = 10000;

    shape_size = 10.0
    c.clearRect(0, 0, 50, 50);
    c.fillStyle = "red";
    c.font = "30px Arial";
    c.fillText(temp,10,50);
    // Accessing coordinates from the coordinates array using forEach loop
    coordinates.forEach(function(coordinate, index) {
        if(index>0)
        {
            c.fillRect(coordinate.x-(shape_size/2), coordinate.y-(shape_size/2), shape_size, shape_size);
            c.moveTo(lastpoint_x,lastpoint_y);
            c.lineTo(coordinate.x,coordinate.y);
            c.stroke();
        } else {
            c.fillRect(coordinate.x-(shape_size/2), coordinate.y-(shape_size/2), shape_size, shape_size);

        }
        lastpoint_x = coordinate.x;
        lastpoint_y = coordinate.y;
    });
}

function draw_polygon() {
    c.clearRect(0, 0, canvas.width, canvas.height);
    c.fillText(temp,10,50);
    c.strokeStyle = "red";
    c.beginPath();
    c.moveTo(coordinates[0].x,coordinates[0].y);

    for(let i = 1; i < coordinates.length; i++) {
        c.lineTo(coordinates[i].x,coordinates[i].y);
    }
    
    c.closePath();
    c.stroke();
}

setInterval(draw, 1000 / 60);