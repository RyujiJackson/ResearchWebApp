var canvas = document.getElementById("myCanvas");
var c  = canvas.getContext("2d");
var sourceImage = document.getElementById("sourceImage");
var zoomButton = document.getElementById("zoom-button");
var canvasContainer = document.getElementById("canvas-container");
var preventZoom = true;

let currentZoom = 1;
let minZoom = 0.8; 
let maxZoom = 5; 
let stepSize = 0.07;
let scale = 1;
let offsetX = 0;
let offsetY = 0;
var isMouseDown = false;
var prevMouseX, prevMouseY;

canvasContainer.addEventListener('mousemove', handleMouseMove);
canvasContainer.addEventListener('mouseup', handleMouseUp);
canvasContainer.addEventListener('mousedown', handleMouseDown);
//to prevent panning when drawingButton clicked
zoomButton.addEventListener('click', toggleZoom);

//function to handle enabling/disabling zooming
function toggleZoom() {
    preventZoom = !preventZoom;

    if(!preventZoom) {
        zoomButton.textContent = "Enabling Zoom";
    } else {
        zoomButton.textContent = "Disabling Zoom";
    }
}

canvas.addEventListener('wheel', function(event) {
    if (!preventZoom) {
        /*
        //old code to apply zoom
        event.preventDefault(); // Prevent default scrolling behavior

        const deltaY = event.deltaY;
        const changeScale = (delta) => {
            scale = Math.max(0.5, Math.min(1.5, scale * Math.exp(delta * 0.0004)));
                
        }
        changeScale(deltaY)
        
        applyZoom();
        */
        //new code to apply zoom
        event.preventDefault(); // Prevent default scrolling behavior
        let direction = event.deltaY > 0 ? -1 : 1; 
        zoomImage(direction); 
        
        
    }
});

//new function to apply zoom
function zoomImage(direction) { 
    let newZoom = currentZoom + direction * stepSize; 
  
    // Limit the zoom level to the minimum and maximum values 
    if (newZoom < minZoom || newZoom > maxZoom) { 
        return; 
    } 
  
    currentZoom = newZoom; 
  
    // Update the CSS transform of the image to scale it 
    canvas.style.transform = 'scale(' + currentZoom + ')'; 
    sourceImage.style.transform = 'scale(' + currentZoom + ')'; 
}

/*
// old Function to apply zoom
function applyZoom() {
    canvas.style.transform = `scale(${scale})`;
    //canvas.style.transformOrigin = 'top left';
    sourceImage.style.transform = `scale(${scale})`;
    //sourceImage.style.transformOrigin = 'top left';

    // Adjust offset to keep the panning consistent with zooming
    offsetX *= scale;
    offsetY *= scale;
    applyPan();
}*/

function applyPan() {
    sourceImage.style.left = offsetX + 'px';
    sourceImage.style.top = offsetY + 'px';
    canvas.style.left = offsetX + 'px';
    canvas.style.top = offsetY + 'px';
}

// Function to handle mouse down event for panning
function handleMouseDown(event) {
    if (window.globalState.preventDrawing && event.button === 0) { // Check if left mouse button is pressed
        isMouseDown = true;
        prevMouseX = event.clientX;
        prevMouseY = event.clientY;
        event.preventDefault();
    }
}

function handleMouseMove(event) {
    if (window.globalState.preventDrawing && isMouseDown) {
        let deltaX = event.clientX - prevMouseX;
        let deltaY = event.clientY - prevMouseY;
        prevMouseX = event.clientX;
        prevMouseY = event.clientY;
        offsetX += deltaX;
        offsetY += deltaY;
        applyPan();
    }
}

function handleMouseUp(event) {
    if (event.button === 0) {
        isMouseDown = false;
    }
}