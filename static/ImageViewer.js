var canvas = document.getElementById("myCanvas");
var c  = canvas.getContext("2d");
var sourceImage = document.getElementById("sourceImage");

let scale = 1;

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
    canvas.style.transformOrigin = 'top left';
    sourceImage.style.transform = `scale(${scale})`;
    sourceImage.style.transformOrigin = 'top left';
}
