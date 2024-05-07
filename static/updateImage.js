function updateImage() {
    var imgIndex = document.querySelector('input[name="to_get_img_index"]').value;
    var window_level = $("#window_level").val();
    var window_width = $("#window_width").val();
    $.ajax({
        url: "/update_image",
        type: "POST",
        data: {
            window_level: window_level,
            window_width: window_width,
            imgIndex: imgIndex
        },
        success: function(data) {
            $('#sourceImage').attr("src", "data:image/png:base64," + data);
            console.log(imgIndex)
        },
        error: function(jqXHR, textStatus, errorThrown) {
          console.error("Error:", textStatus, errorThrown);
          // Handle errors gracefully, e.g., display an error message
        }
    });
}