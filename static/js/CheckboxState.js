(function() {
  var cbstate = {};

  window.addEventListener('load', function() {
      // Check if localStorage has stored checkbox states
      if (localStorage.getItem('CBState')) {
          cbstate = JSON.parse(localStorage.getItem('CBState'));
      }

      // Loop through the stored states and restore them
      for (var name in cbstate) {
          var el = document.querySelector('input[name="' + name + '"]');
          if (el) {
              el.checked = cbstate[name];  // Restore the checked state
          }
      }

      // Get all checkboxes with a specific class that we want to monitor
      var checkboxes = document.querySelectorAll('input[type="checkbox"]');

      checkboxes.forEach(function(cb) {
          // Bind click event to each checkbox to monitor its state
          cb.addEventListener('change', function() {
              if (this.checked) {
                  cbstate[this.name] = true;  // Mark as checked
              } else {
                  delete cbstate[this.name];  // Remove from saved state if unchecked
              }

              // Save the updated state to localStorage
              localStorage.setItem('CBState', JSON.stringify(cbstate));
          });
      });
  });
})();