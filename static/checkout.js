document.getElementById('confirm').addEventListener('click', function() {
    storeName();
    window.location.href = '/confirmation';
});

function storeName() {
    let name = document.getElementById('name').value;
    localStorage.setItem('userName', name); 
}

document.addEventListener('DOMContentLoaded', function() {
    const confirmButton = document.getElementById('confirm');
    confirmButton.disabled = true; // Disable the button initially

    // Function to set error message
    function setError(inputId, message) {
        const errorSpan = document.getElementById(inputId + '-error');
        if (errorSpan) {
            errorSpan.textContent = message;
        } else {
            console.error("Error element not found for:", inputId);
        }
    }

    // Function to clear error message
    function clearError(inputId) {
        setError(inputId, '');
    }

    // Function to check if all fields are valid
    function validateForm() {
        let isValid = true;

        // Name validation
        const name = document.getElementById('name').value;
        if (!name.trim()) {
            setError('name', 'Name is required.');
            isValid = false;
        } else {
            clearError('name');
        }

        // Address validation
        const address = document.getElementById('address').value;
        if (!address.trim()) {
            setError('address', 'Address is required.');
            isValid = false;
        } else {
            clearError('address');
        }

        // Telephone validation
        const telephone = document.getElementById('telephone').value;
        if (!telephone.trim()) {
            setError('telephone', 'Telephone is required.');
            isValid = false;
        } else {
            clearError('telephone');
        }

        // Card number validation (16 digits)
        const cardNumber = document.getElementById('card_number').value;
        if (!/^\d{16}$/.test(cardNumber)) {
            setError('card_number', 'Card number must be 16 digits.');
            isValid = false;
        } else {
            clearError('card_number');
        }

        // Expiry date validation (MM/YY)
        const expiryDate = document.getElementById('expiry_date').value;
        if (!/^(0[1-9]|1[0-2])\/[0-9]{2}$/.test(expiryDate)) {
            setError('expiry_date', 'Expiry date must be in MM/YY format.');
            isValid = false;
        } else {
            clearError('expiry_date');
        }

        // CVC validation (3 digits)
        const cvc = document.getElementById('cvc').value;
        if (!/^\d{3}$/.test(cvc)) {
            setError('cvc', 'CVC must be 3 digits.');
            isValid = false;
        } else {
            clearError('cvc');
        }

        confirmButton.disabled = !isValid;
    }

    // Add event listeners to all input fields
    document.querySelectorAll('.billing-section input, .payment-methods input').forEach(input => {
        input.addEventListener('input', validateForm);
    });
});
