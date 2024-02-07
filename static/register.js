document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('registerForm').addEventListener('submit', function(event) {
        if (!validatePassword()) {
            event.preventDefault();
        }
    });
});

function validatePassword() {
    var password = document.getElementById("password").value;
    var errorText = "";
    var isValid = true;

    if (password.length < 8) {
        errorText = "Password must be at least 8 characters long.";
        isValid = false;
    }
    // Add more validation checks as per your requirements

    document.getElementById("passwordError").innerText = errorText;
    return isValid;
}