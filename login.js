document.addEventListener('DOMContentLoaded', function() {
    // Show the login/signup form after 5 seconds
    setTimeout(function() {
        document.getElementById('auth-modal').style.display = 'block';
    }, 5000);

    // Handle form submission
    document.getElementById('auth-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form from submitting the traditional way

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Simple validation (replace with actual validation/authorization logic)
        if (username && password) {
            alert('Login/Signup successful!');
            
            // Hide the form and show the main content
            document.getElementById('auth-modal').style.display = 'none';
            document.getElementById('main-content').style.display = 'block';
        } else {
            alert('Please fill in all fields');
        }
    });
});
