var canvas = document.getElementById("myCanvas");
var c  = canvas.getContext("2d");
var sourceImage = document.getElementById("sourceImage");
var preventPanning = false;

let scale = 1;
let offsetX = 0;
let offsetY = 0;
var isMouseDown = false;
var prevMouseX, prevMouseY;

document.addEventListener('mousemove', handleMouseMove);
document.addEventListener('mouseup', handleMouseUp);
canvas.addEventListener('mousedown', handleMouseDown);
//to prevent panning when drawingButton clicked
drawingButton.addEventListener('click', togglePanning);

document.getElementById('zoom-in').addEventListener('click', function() {
    scale += 0.1;
    applyZoom();
});

// Function to handle zoom out
document.getElementById('zoom-out').addEventListener('click', function() {
    scale -= 0.1;
    applyZoom();
});

// Function to apply zoom
function applyZoom() {
    canvas.style.transform = `scale(${scale})`;
    //canvas.style.transformOrigin = 'top left';
    sourceImage.style.transform = `scale(${scale})`;
    //sourceImage.style.transformOrigin = 'top left';

    // Adjust offset to keep the panning consistent with zooming
    offsetX *= scale;
    offsetY *= scale;
    applyPan();
}

function applyPan() {
    sourceImage.style.left = offsetX + 'px';
    sourceImage.style.top = offsetY + 'px';
    canvas.style.left = offsetX + 'px';
    canvas.style.top = offsetY + 'px';
}

// Function to handle mouse down event for panning
function handleMouseDown(event) {
    if (!preventPanning && event.button === 0) { // Check if left mouse button is pressed
        isMouseDown = true;
        prevMouseX = event.clientX;
        prevMouseY = event.clientY;
        event.preventDefault();
    }
}

function handleMouseMove(event) {
    if (!preventPanning && isMouseDown) {
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

function togglePanning() {
    preventPanning = !preventPanning; // Toggle the prevent flag
  // Optionally change button text based on state (active/inactive)
  if (preventPanning) {
    toggleButton.textContent = "Enable Panning";
  } else {
    toggleButton.textContent = "Disable Panning";
  }
}

