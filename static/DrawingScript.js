//script to handle drawing area of H.Pylori Infection
var canvas = document.getElementById("myCanvas");
var c  = canvas.getContext("2d");
var mouse_on_canvas = {x:0, y:0};
var temp = 0;
const coordinates = [];
var timer = 0
var delay = 200
var prevent = false

window.addEventListener('click', onClick);
window.addEventListener('dblclick', doubleClick);

function onClick(event) {
    timer = setTimeout(() => {
        if(!prevent){

            var rect = canvas.getBoundingClientRect();
            mouse_on_canvas.x = event.clientX - rect.left;
            mouse_on_canvas.y = event.clientY - rect.top;
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
        prevent = false
    }, delay)
    
}

function doubleClick(event) {
    clearTimeout(timer)
    prevent=true

    var rect = canvas.getBoundingClientRect();
    mouse_on_canvas.x = event.clientX - rect.left;
    mouse_on_canvas.y = event.clientY - rect.top;
    if(((event.clientX >= rect.left) && (event.clientY >= rect.top)))
    {
        if(((event.clientX <= rect.right)  && (event.clientY <= rect.bottom)))
        {
            draw_polygon()
        }
    }
}

function draw() {
    var lastpoint_x = 1000;
    var lastpoint_y = 1000;

    shape_size = 10.0
    c.clearRect(0, 0, canvas.width, canvas.height);
    c.fillStyle = "red";
    //c.fillRect(mouse_on_canvas.x-(shape_size/2), mouse_on_canvas.y-(shape_size/2), shape_size, shape_size);
    c.font = "30px Arial";
    c.fillText(temp,10,50);
    // Accessing coordinates from the coordinates array using forEach loop
    coordinates.forEach(function(coordinate, index) {
        //x = String(coordinate.x);
        //y = String(coordinate.y);
        //c.fillText(x + " " + y,10,50+(30*(index+1)))
        
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
    //c.fillRect(mouse_on_canvas.x-(shape_size/2), mouse_on_canvas.y-(shape_size/2), shape_size, shape_size);
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

