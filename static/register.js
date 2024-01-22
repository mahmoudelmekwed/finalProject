
$(document).ready(() => {
    let isEmailValid = true;
    let isUsernameValid = true;

    // Email validation
    $('#emailField').on('input', function() {
        let email = $(this).val();
        $.ajax({
            url: '/check-email',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({email: email}),
            success: function(response) {
                if(response.exists) {
                    $('#emailError').text('Email already in use.');
                    isEmailValid = false;
                } else {
                    $('#emailError').text('');
                    isEmailValid = true;
                }
            }
        });
    });

    // Username validation
    $('#nameField').on('input', function() {
        let username = $(this).val();
        $.ajax({
            url: '/check-username',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({username: username}),
            success: function(response) {
                if(response.exists) {
                    $('#usernameError').text('Username already in use.');
                    isUsernameValid = false;
                } else {
                    $('#usernameError').text('');
                    isUsernameValid = true;
                }
            }
        });
    });

    // Prevent form submission if the email or username is invalid
    $('#registerForm').submit(function(e) {
        if (!isEmailValid || !isUsernameValid) {
            e.preventDefault();
            $('#submissionError').text('Please correct the errors before submitting.');
        } else {
            $('#submissionError').text('');
        }
    });
});