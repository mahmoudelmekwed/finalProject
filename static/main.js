function updateTotalPrice(productId) {
    let pricePerUnit = parseFloat(document.getElementById('price-'+productId).getAttribute('data-price-per-unit'));
    let quantity = parseInt(document.getElementById('quantity-'+productId).value);
    let totalPrice = pricePerUnit * quantity;
    document.getElementById('price-'+productId).innerText = totalPrice.toFixed(2);
    localStorage.setItem('quantity-'+productId , quantity);
}


function checkForUpdates() {
    let productIds = [1,2,3,4,5,6,7,8,9,10,11,12]; 
    productIds.forEach(function(productId) {
        let savedQuantity = localStorage.getItem('quantity-' + productId);
        let quantityElement = document.getElementById('quantity-' + productId);
        if (savedQuantity && quantityElement && quantityElement.value !== savedQuantity) {
            quantityElement.value = savedQuantity;
            updateTotalPrice(productId);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    checkForUpdates();
    setInterval(checkForUpdates, 1000); 
});

document.getElementById('registerForm').addEventListener('input', function(event) {
    var password = document.getElementById('password').value;
    var errors = [];

    if (password.length < 8) {
        errors.push("Password must be at least 8 characters long.");
    }
    if (!password.match(/[A-Z]/)) {
        errors.push("Password must contain at least one uppercase letter.");
    }
    if (!password.match(/[a-z]/)) {
        errors.push("Password must contain at least one lowercase letter.");
    }
    if (!password.match(/[0-9]/)) {
        errors.push("Password must contain at least one digit.");
    }
    if (!password.match(/[^a-zA-Z0-9]/)) {
        errors.push("Password must contain at least one special character.");
    }

    if (errors.length > 0) {
        document.getElementById('passwordError').innerHTML = errors.join("<br>");
        event.preventDefault();
    }
});


$(document).ready(function() {
    $('#emailField').on('input', function() {
        var email = $(this).val();
        $.ajax({
            url: '/check-email',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({email: email}),
            success: function(response) {
                if(response.exists) {
                    $('#emailError').text('Email already in use.');
                } else {
                    $('#emailError').text('');
                }
            }
        });
    });
});
