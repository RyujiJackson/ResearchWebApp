var filenameProcessed = false;
var filename;

function updateImage() {
    if(!filenameProcessed)
        {
            filename = $('#sourceImage').attr("src").split('/').pop(); // Extract filename from sourceImage src attribute
            filename = filename.replace(/\.png$/i, ".DCM");
            filenameProcessed = true; // Set flag after processing
        }
    var window_level = $("#window_level").val();
    var window_width = $("#window_width").val();
    $.ajax({
        url: "/update_image",
        type: "POST",
        data: {
            window_level: window_level,
            window_width: window_width,
            filename: filename
        },
        success: function(data) {
            $('#sourceImage').attr("src", "data:image/png:base64," + data);
            //alert(filename);
        },
        error: function(jqXHR, textStatus, errorThrown) {
          console.error("Error:", textStatus, errorThrown);
          //alert(filename);
          // Handle errors gracefully, e.g., display an error message
        }
    });
}

