$(document).ready(function() {
    $('#loginBtn').on('click', function() {
        const username = $('#username').val();
        const password = $('#password').val();

        // Assume this is your API endpoint
        const apiUrl = 'http://127.0.0.1:8000/api/login/';

        // Example payload for login request
        const data = {
            username: username,
            password: password
        };

        // Send a POST request to the API
        $.post(apiUrl, data)
            .done(function() {
                // On successful login, redirect to data-tables.html
                window.location.href = 'data-tables.html';
            })
            .fail(function() {
                // On failed attempt, show an error message
                alert('Invalid credentials');
            });
    });

    $('#registerBtn').on('click', function() {
        window.location.href = 'register.html';
    });
});
