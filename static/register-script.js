$(document).ready(function() {
    $('#loginBtn').on('click', function() {
        const username = $('#username').val();
        const password = $('#password').val();
        const email = $('#email').val();

        // Assume this is your API endpoint
        const apiUrl = 'http://127.0.0.1:8000/api/register/';

        // Example payload for registration request
        const data = {
            username: username,
            password: password,
            email: email
        };

        // Send a POST request to the API
        $.post(apiUrl, data)
            .done(function() {
                // On successful registration, you can handle the response as needed
                // For example, redirect to a success page or show a success message
                alert('Registration successful!');

                // On successful registration, redirect to data-tables.html
                window.location.href = 'data-tables.html';
            })
            .fail(function() {
                // On failed registration, show an error message
                alert('Registration failed. Please try again.');
            });
    });
});

function submitForm() {
    // Validation checks for password match
    var password = document.getElementById("password").value;
    var retypePassword = document.getElementById("retype-password").value;
    var passwordMatchError = document.getElementById("password-match-error");

    if (password !== retypePassword) {
        passwordMatchError.textContent = "Passwords do not match";
        return;
    } else {
        passwordMatchError.textContent = "";
    }
}