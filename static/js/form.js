$(document).ready(function() {
    // Intercept form submission
    $('#my-form').submit(function(event) {
        event.preventDefault(); // Prevent default form submission
        
        // Serialize form data
        var formData = $(this).serialize();
        
        // Submit form data asynchronously via AJAX
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'), // Form action URL
            data: formData, // Serialized form data
            success: function(response) {
                // Display success message
                $('#message-container').text('Form submitted successfully!');
            },
            error: function(xhr, errmsg, err) {
                // Display error message
                $('#message-container').text('An error occurred while submitting the form.');
            }
        });
    });
  });
  