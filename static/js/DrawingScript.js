//script to handle drawing area of H.Pylori Infection
var canvas = document.getElementById("myCanvas");
var c  = canvas.getContext("2d");
var undoButton = document.getElementById("undo")
var drawingButton = document.getElementById("drawing-toggle")
var mouse_on_canvas = {x:0, y:0};
var temp = 0;
const coordinates = [];
const fold_coord = [];
const corpus_coord = [];
const antrum_coord = [];
var annotation_color;
var annotation_filename;



const imgIndex = document.querySelector('input[name="img_index"]').value;
canvas.addEventListener('click', onClick);
canvas.addEventListener('contextmenu', rightClick);
undoButton.addEventListener('click', undoClick);
drawingButton.addEventListener('click', toggleDrawing);
var dropDownValue = document.getElementById("options").value;


function toggleDrawing() {
  change_anntotaion_type();
    window.globalState.preventDrawing = !window.globalState.preventDrawing;
    if (!window.globalState.preventDrawing) {
        drawingButton.textContent = "Enabling Drawing";
      } else if(window.globalState.preventDrawing){
        drawingButton.textContent = "Disabling Drawing";
      }
}

function onClick(event) {
    if(!window.globalState.preventDrawing){
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
                coordinates.push({ x: mouse_on_canvas.x, y: mouse_on_canvas.y });
                draw()
            }
        }

    }
}

function rightClick(event) {
  event.preventDefault();
    if (coordinates.length > 2) {
        window.globalState.preventDrawing=true;
        if (!window.globalState.preventDrawing) {
            drawingButton.textContent = "Enabling Drawing";
          } else if(window.globalState.preventDrawing){
            drawingButton.textContent = "Disabling Drawing";
          }

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

function undoClick() {
    if (coordinates.length > 0) {
        temp--;
        coordinates.pop(); // Remove the last point from the coordinates array
        c.reset(); // context reset
        /*
        window.globalState.preventDrawing = false; // to handle when undo right click
        if (!window.globalState.preventDrawing) {
            drawingButton.textContent = "Enabling Drawing";
          } else if(window.globalState.preventDrawing){
            drawingButton.textContent = "Disabling Drawing";
          }
          */
         change_anntotaion_type()
        draw(); // Redraw the canvas without the removed point
    }
}

function draw() {
    var lastpoint_x = 10000;
    var lastpoint_y = 10000;

    shape_size = 5.0
    //c.clearRect(0, 0, 50, 50);
    
    
    //c.font = "30px Arial";
    //c.fillText(mouse_on_canvas.x,10,50);
    //c.fillText(mouse_on_canvas.y,10,100);

    // Accessing coordinates from the coordinates array using forEach loop
    coordinates.forEach(function(coordinate, index) {
        c.fillStyle = annotation_color;
        c.strokeStyle = annotation_color;
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
    //c.clearRect(0, 0, canvas.width, canvas.height);
    //c.fillText(temp,10,50);
    c.strokeStyle = annotation_color;
    c.fillStyle = annotation_color;
    c.beginPath();
    c.moveTo(coordinates[0].x,coordinates[0].y);

    for(let i = 1; i < coordinates.length; i++) {
        c.lineTo(coordinates[i].x,coordinates[i].y);
    }
    
    c.closePath();
    c.stroke();
    saveArray(coordinates);
}

//save array
async function saveArray(arrayData) {
    try {
      const response = await fetch("/save_array", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ array: arrayData ,imgIndex,annotation_filename}),
      });
  
      if (!response.ok) {
        throw new Error(`Error saving array: ${response.statusText}`);
      }
  
      const data = await response.json();
      console.log(data.message);  // Handle success message
    } catch (error) {
      console.error("Error:", error);  // Handle errors
    }
  }

function change_anntotaion_type(){
  if(dropDownValue==0)
    {
      annotation_color = "red";
      annotation_filename = "fold.txt";
    }
  else if(dropDownValue==1)
    {
      annotation_color = "green";
      annotation_filename = "corpus.txt";
    }
  else if(dropDownValue==2)
    {
      annotation_color = "blue";
      annotation_filename = "antrum.txt";
    }
}

setInterval(draw, 1000 / 60);