function updateImage() {
    const imgIndex = document.querySelector('input[name="to_get_img_index"]').value;
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
            str = JSON.stringify(data, null, 4); // (Optional) beautiful indented output.
            console.log(data.image_data_url); // Logs output to dev tools console.
            //alert(str); // Displays output using window.alert()
            
            //$('#processed_image').attr('src', data.image_data_url);
            //$('#processed_image').attr('src', "../static/uploads/origin/20150414000010002.png");
            $('#sourceImage').attr('src', data.image_data_url);
            $('#sourceImage').attr('src', "../static/uploads/origin/20150414000010002.png");
        },
        error: function(jqXHR, textStatus, errorThrown) {
          console.error("Error:", textStatus, errorThrown);
          // Handle errors gracefully, e.g., display an error message
        }
    });
}